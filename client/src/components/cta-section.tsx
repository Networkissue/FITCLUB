import { Button } from "@/components/ui/button";
import { Rocket, Calendar } from "lucide-react";

export default function CTASection() {
  return (
    <section className="py-20 bg-gradient-to-r from-primary-custom to-accent">
      <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
        <h2 className="text-5xl font-black text-white mb-6">
          Ready to Transform Your Physique?
        </h2>
        <p className="text-xl text-white mb-8 leading-relaxed">
          Join thousands of athletes who have achieved their body composition goals with our science-based nutrition plans
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button className="bg-white text-primary-custom px-8 py-4 rounded-full text-lg font-bold transition-all duration-200 transform hover:scale-105 shadow-lg hover:shadow-xl hover:bg-gray-100">
            <Rocket className="mr-2 h-5 w-5" />
            Start Free Trial
          </Button>
          <Button 
            variant="outline"
            className="border-2 border-white text-white px-8 py-4 rounded-full text-lg font-bold transition-all duration-200 transform hover:scale-105 hover:bg-white hover:text-primary-custom bg-transparent"
          >
            <Calendar className="mr-2 h-5 w-5" />
            Book Consultation
          </Button>
        </div>
      </div>
    </section>
  );
}
