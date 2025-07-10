import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Dumbbell, Menu, X } from "lucide-react";
import gymLogo from "@assets/3d gym_1752142046400.png";

export default function Navigation() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      setIsScrolled(scrollTop > 100);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    setIsMenuOpen(false);
  };

  return (
    <nav className={`bg-white shadow-lg fixed w-full top-0 z-50 nav-transition ${isScrolled ? 'transform-none' : ''}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center">
              <img 
                src={gymLogo} 
                alt="The Gym by Johnson" 
                className="h-12 w-auto"
              />
            </div>
          </div>
          
          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <button 
              onClick={() => scrollToSection('home')}
              className="text-dark-custom hover:text-primary-custom transition-colors duration-200 font-medium"
            >
              Home
            </button>
            <button 
              onClick={() => scrollToSection('bulking')}
              className="text-dark-custom hover:text-primary-custom transition-colors duration-200 font-medium"
            >
              Bulking
            </button>
            <button 
              onClick={() => scrollToSection('cutting')}
              className="text-dark-custom hover:text-primary-custom transition-colors duration-200 font-medium"
            >
              Cutting
            </button>
            <button 
              onClick={() => scrollToSection('nutrition')}
              className="text-dark-custom hover:text-primary-custom transition-colors duration-200 font-medium"
            >
              Nutrition
            </button>
            <Button 
              onClick={() => scrollToSection('contact')}
              className="bg-primary-custom text-white px-6 py-2 rounded-full hover:bg-orange-600 transition-colors duration-200 font-medium"
            >
              Get Started
            </Button>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-dark-custom hover:text-primary-custom"
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white border-t">
              <button 
                onClick={() => scrollToSection('home')}
                className="block w-full text-left px-3 py-2 text-dark-custom hover:text-primary-custom transition-colors duration-200 font-medium"
              >
                Home
              </button>
              <button 
                onClick={() => scrollToSection('bulking')}
                className="block w-full text-left px-3 py-2 text-dark-custom hover:text-primary-custom transition-colors duration-200 font-medium"
              >
                Bulking
              </button>
              <button 
                onClick={() => scrollToSection('cutting')}
                className="block w-full text-left px-3 py-2 text-dark-custom hover:text-primary-custom transition-colors duration-200 font-medium"
              >
                Cutting
              </button>
              <button 
                onClick={() => scrollToSection('nutrition')}
                className="block w-full text-left px-3 py-2 text-dark-custom hover:text-primary-custom transition-colors duration-200 font-medium"
              >
                Nutrition
              </button>
              <Button 
                onClick={() => scrollToSection('contact')}
                className="w-full mt-2 bg-primary-custom text-white hover:bg-orange-600 transition-colors duration-200 font-medium"
              >
                Get Started
              </Button>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}
