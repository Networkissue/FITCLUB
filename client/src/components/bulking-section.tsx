import { Card, CardContent } from "@/components/ui/card";
import { TrendingUp, Calculator, Dumbbell, Clock, Leaf } from "lucide-react";

export default function BulkingSection() {
  const bulkingMeals = [
    {
      id: 1,
      title: "Whole Milk and Cottage Cheese",
      description: "High-protein dairy combination for muscle building",
      calories: "850 cal",
      protein: "45g protein",
      image: "https://images.unsplash.com/photo-1571212515416-fbbf4fb2e811?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&h=600"
    },
    {
      id: 2,
      title: "Nuts and Nut Butters",
      description: "Calorie-dense healthy fats and proteins",
      calories: "720 cal",
      protein: "25g protein",
      image: "https://images.unsplash.com/photo-1559656914-a30970c1affd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&h=600"
    },
    {
      id: 3,
      title: "Whole Eggs",
      description: "Complete protein with essential amino acids",
      calories: "680 cal",
      protein: "42g protein",
      image: "https://images.unsplash.com/photo-1506354666786-959d6d497f1a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&h=600"
    },
    {
      id: 4,
      title: "Rice",
      description: "Complex carbohydrates for energy and recovery",
      calories: "450 cal",
      protein: "8g protein",
      image: "https://images.unsplash.com/photo-1586201375761-83865001e31c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&h=600"
    },
    {
      id: 5,
      title: "Chicken and Mutton",
      description: "Lean protein sources for muscle development",
      calories: "650 cal",
      protein: "65g protein",
      image: "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&h=600"
    }
  ];

  const features = [
    {
      icon: Calculator,
      title: "3000+ Calories",
      description: "Daily caloric surplus for optimal muscle growth"
    },
    {
      icon: Dumbbell,
      title: "180g+ Protein",
      description: "High protein intake for muscle synthesis"
    },
    {
      icon: Clock,
      title: "6 Meals Daily",
      description: "Frequent meals for steady nutrition"
    },
    {
      icon: Leaf,
      title: "Clean Bulking",
      description: "Quality nutrients for lean muscle gain"
    }
  ];

  return (
    <section id="bulking" className="py-20 bg-gradient-to-br from-orange-50 to-red-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-5xl font-black text-dark-custom mb-6">
            <TrendingUp className="inline-block text-primary-custom mr-4 h-12 w-12" />
            Bulking Diet Plans
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Maximize muscle growth with our scientifically-designed bulking meal plans. 
            High-calorie, nutrient-dense foods to fuel your gains.
          </p>
        </div>

        {/* Bulking Meal Examples Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {bulkingMeals.map((meal) => (
            <Card key={meal.id} className="bg-white rounded-2xl shadow-xl overflow-hidden transform hover:scale-105 transition-all duration-300">
              <img 
                src={meal.image} 
                alt={meal.title} 
                className="w-full h-48 object-cover"
              />
              <CardContent className="p-6">
                <h3 className="text-xl font-bold text-dark-custom mb-2">{meal.title}</h3>
                <p className="text-gray-600 mb-4">{meal.description}</p>
                <div className="flex justify-between items-center">
                  <span className="text-2xl font-black text-primary-custom">{meal.calories}</span>
                  <span className="text-sm font-medium text-secondary-custom">{meal.protein}</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Bulking Plan Features */}
        <Card className="bg-white rounded-3xl shadow-2xl p-8 md:p-12">
          <h3 className="text-3xl font-black text-dark-custom mb-8 text-center">Bulking Plan Features</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <div key={index} className="text-center p-6">
                <feature.icon className={`h-12 w-12 mx-auto mb-4 ${index % 2 === 0 ? 'text-primary-custom' : 'text-secondary-custom'}`} />
                <h4 className="text-lg font-bold text-dark-custom mb-2">{feature.title}</h4>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </section>
  );
}
