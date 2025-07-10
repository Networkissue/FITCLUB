import { Card, CardContent } from "@/components/ui/card";
import { Scissors, Flame, Heart, Gauge, Droplets } from "lucide-react";

export default function CuttingSection() {
  const cuttingMeals = [
    {
      id: 1,
      title: "Carbohydrates",
      description: "Complex carbs for sustained energy during cuts",
      calories: "320 cal",
      protein: "12g protein",
      image: "https://images.unsplash.com/photo-1586201375761-83865001e31c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&h=600"
    },
    {
      id: 2,
      title: "Lean Fish",
      description: "Low-calorie, high-protein white fish",
      calories: "280 cal",
      protein: "45g protein",
      image: "https://images.unsplash.com/photo-1485963631004-f2f00b1d6606?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&h=600"
    },
    {
      id: 3,
      title: "Eggs",
      description: "High-quality protein with essential nutrients",
      calories: "180 cal",
      protein: "24g protein",
      image: "https://images.unsplash.com/photo-1525351484163-7529414344d8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&h=600"
    },
    {
      id: 4,
      title: "Dairy",
      description: "Low-fat dairy products for protein",
      calories: "250 cal",
      protein: "28g protein",
      image: "https://images.unsplash.com/photo-1571212515416-fbbf4fb2e811?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&h=600"
    },
    {
      id: 5,
      title: "Pulses (Lentils, Beans, Peas)",
      description: "Plant-based protein and fiber",
      calories: "200 cal",
      protein: "18g protein",
      image: "https://images.unsplash.com/photo-1586795158095-e891c9e1a42b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&h=600"
    },
    {
      id: 6,
      title: "Tofu, Seeds & Nuts",
      description: "Plant-based proteins and healthy fats",
      calories: "290 cal",
      protein: "22g protein",
      image: "https://images.unsplash.com/photo-1559656914-a30970c1affd?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&h=600"
    }
  ];

  const features = [
    {
      icon: Flame,
      title: "1800-2200 Calories",
      description: "Caloric deficit for fat loss"
    },
    {
      icon: Heart,
      title: "150g+ Protein",
      description: "Muscle preservation during cut"
    },
    {
      icon: Gauge,
      title: "Low Carb Focus",
      description: "Strategic carb timing"
    },
    {
      icon: Droplets,
      title: "High Volume",
      description: "Filling, low-calorie foods"
    }
  ];

  return (
    <section id="cutting" className="py-20 bg-gradient-to-br from-blue-50 to-indigo-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-5xl font-black text-dark-custom mb-6">
            <Scissors className="inline-block text-secondary-custom mr-4 h-12 w-12" />
            Cutting Diet Plans
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Shed fat while preserving muscle with our precision cutting meal plans. 
            Low-calorie, high-protein foods for lean physique goals.
          </p>
        </div>

        {/* Cutting Meal Examples Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
          {cuttingMeals.map((meal) => (
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
                  <span className="text-2xl font-black text-secondary-custom">{meal.calories}</span>
                  <span className="text-sm font-medium text-primary-custom">{meal.protein}</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Cutting Plan Features */}
        <Card className="bg-white rounded-3xl shadow-2xl p-8 md:p-12">
          <h3 className="text-3xl font-black text-dark-custom mb-8 text-center">Cutting Plan Features</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <div key={index} className="text-center p-6">
                <feature.icon className={`h-12 w-12 mx-auto mb-4 ${index % 2 === 0 ? 'text-secondary-custom' : 'text-primary-custom'}`} />
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
