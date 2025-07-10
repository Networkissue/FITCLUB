import { Button } from "@/components/ui/button";
import { TrendingUp, Scissors } from "lucide-react";

export default function HeroSection() {
  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <section id="home" className="pt-16">
      <div 
        className="relative h-screen bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80')`
        }}
      >
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center text-white max-w-4xl mx-auto px-4">
            <h1 className="text-5xl md:text-7xl font-black mb-6 leading-tight">
              Transform Your Body with{" "}
              <span className="text-primary-custom heighlight">Johnson</span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 font-light leading-relaxed">
              Professional diet plans designed for bulking and cutting phases. 
              Achieve your fitness goals with our expert-crafted nutrition strategies.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                onClick={() => scrollToSection('bulking')}
                className="bg-primary-custom hover:bg-orange-600 text-white px-8 py-4 rounded-full text-lg font-semibold transition-all duration-200 transform hover:scale-105 shadow-lg"
                size="lg"
              >
                <TrendingUp className="mr-2 h-5 w-5" />
                Start Bulking Plan
              </Button>
              <Button 
                onClick={() => scrollToSection('cutting')}
                className="bg-secondary-custom hover:bg-blue-700 text-white px-8 py-4 rounded-full text-lg font-semibold transition-all duration-200 transform hover:scale-105 shadow-lg"
                size="lg"
              >
                <Scissors className="mr-2 h-5 w-5" />
                Start Cutting Plan
              </Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
