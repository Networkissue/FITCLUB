import { Card, CardContent } from "@/components/ui/card";
import { FlaskConical, CheckCircle } from "lucide-react";

export default function NutritionSection() {
  const evidencePoints = [
    {
      title: "Metabolic Flexibility",
      description: "Our plans adapt to your body's changing needs during different phases"
    },
    {
      title: "Nutrient Timing",
      description: "Strategic meal timing to optimize performance and recovery"
    },
    {
      title: "Bioavailability",
      description: "Food combinations that maximize nutrient absorption"
    }
  ];

  const nutritionCategories = [
    {
      title: "Micronutrients",
      description: "Essential vitamins and minerals for optimal health",
      image: "https://images.unsplash.com/photo-1619566636858-adf3ef46400b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&h=300",
      gradient: "from-orange-50 to-red-50"
    },
    {
      title: "Hydration",
      description: "Optimal water intake for performance and recovery",
      image: "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&h=300",
      gradient: "from-blue-50 to-indigo-50"
    },
    {
      title: "Healthy Fats",
      description: "Omega-3s for inflammation control and hormone support",
      image: "https://images.unsplash.com/photo-1509440159596-0249088772ff?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&h=300",
      gradient: "from-green-50 to-emerald-50"
    },
    {
      title: "Antioxidants",
      description: "Protection against exercise-induced oxidative stress",
      image: "https://images.unsplash.com/photo-1506806732259-39c2d0268443?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=400&h=300",
      gradient: "from-purple-50 to-pink-50"
    }
  ];

  return (
    <section id="nutrition" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-5xl font-black text-dark-custom mb-6">
            <FlaskConical className="inline-block text-accent mr-4 h-12 w-12" />
            Nutrition Science
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Our meal plans are backed by the latest nutrition research and sports science
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mb-16">
          <div>
            <img 
              src="https://images.unsplash.com/photo-1559757148-5c350d0d3c56?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&h=600" 
              alt="Nutrition science laboratory" 
              className="rounded-2xl shadow-2xl w-full h-auto"
            />
          </div>
          <div>
            <h3 className="text-3xl font-black text-dark-custom mb-6">Evidence-Based Approach</h3>
            <div className="space-y-6">
              {evidencePoints.map((point, index) => (
                <div key={index} className="flex items-start">
                  <CheckCircle className="text-green-500 h-6 w-6 mr-4 mt-1 flex-shrink-0" />
                  <div>
                    <h4 className="text-lg font-bold text-dark-custom mb-2">{point.title}</h4>
                    <p className="text-gray-600">{point.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Nutrition Facts Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {nutritionCategories.map((category, index) => (
            <Card key={index} className={`text-center p-6 bg-gradient-to-br ${category.gradient} rounded-2xl border-0`}>
              <CardContent className="p-0">
                <img 
                  src={category.image} 
                  alt={category.title} 
                  className="w-full h-32 object-cover rounded-xl mb-4"
                />
                <h4 className="text-lg font-bold text-dark-custom mb-2">{category.title}</h4>
                <p className="text-gray-600 text-sm">{category.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
