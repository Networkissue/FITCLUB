export default function StatsSection() {
  const stats = [
    { number: "5K+", label: "Success Stories" },
    { number: "100+", label: "Meal Plans" },
    { number: "24/7", label: "Expert Support" },
    { number: "99.9%", label: "Satisfaction Rate" }
  ];

  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
          {stats.map((stat, index) => (
            <div key={index} className="p-6">
              <div className={`text-4xl font-black mb-2 ${index % 2 === 0 ? 'text-primary-custom' : 'text-secondary-custom'}`}>
                {stat.number}
              </div>
              <div className="text-lg font-medium text-gray-600">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
