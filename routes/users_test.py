@signin_router.get("/api/users")
async def api_get_users(request: Request, page: int = Query(1), limit: int = Query(5), search: str = ""):
    user = get_user_by_cookie(request)
    if not user or user.get("role") != "admin":
        return JSONResponse(status_code=403, content={"status": "error", "detail": "Unauthorized"})

    # Always exclude admin users
    base_filter = {"role": {"$ne": "admin"}}

    if search:
        user_ids_with_status = [
            p["user_id"] for p in payment_due.find(
                {"status": {"$regex": search, "$options": "i"}}, {"user_id": 1}
            )
        ]

        # Combine with search filters
        base_filter["$or"] = [
            {"id": {"$regex": search, "$options": "i"}},
            {"username": {"$regex": search, "$options": "i"}},
            {"id": {"$in": user_ids_with_status}}
        ]

    skip = (page - 1) * limit
    users_cursor = user_data.find(base_filter, {
        "_id": 0,
        "id": 1,
        "username": 1,
        "mobile": 1,
        "gender": 1,
        "joining_date": 1,
        "last_payment_date": 1,
        "next_due_date": 1
    }).skip(skip).limit(limit)

    users = list(users_cursor)

    for u in users:
        # Fix datetime fields
        if isinstance(u.get("joining_date"), datetime):
            u["joining_date"] = u["joining_date"].strftime("%Y-%m-%d")
        if isinstance(u.get("last_payment_date"), datetime):
            u["last_payment_date"] = u["last_payment_date"].strftime("%Y-%m-%d")
        if isinstance(u.get("next_due_date"), datetime):
            u["next_due_date"] = u["next_due_date"].strftime("%Y-%m-%d")

        # Add status
        payment = payment_due.find_one({"user_id": u["id"]}, {"_id": 0, "status": 1})
        u["status"] = payment["status"] if payment else "unknown"

        # Add membership
        latest_payment = payment_history.find_one(
            {"user_id": u["id"]},
            sort=[("next_due", -1)],
            projection={"membership": 1}
        )
        u["membership"] = latest_payment["membership"] if latest_payment and "membership" in latest_payment else "NA"

    total_users = user_data.count_documents(base_filter)
    total_pages = (total_users + limit - 1) // limit

    return JSONResponse(status_code=200, content={
        "status": "success",
        "users": users,
        "page": page,
        "total_pages": total_pages,
        "total_users": total_users  # ✅ now excludes admin
    })