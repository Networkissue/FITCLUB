import { Dumbbell, Facebook, Instagram, Youtube, Twitter, Mail, Phone, MapPin } from "lucide-react";
import gymLogo from "@assets/3d gym_1752142046400.png";

export default function Footer() {
  const quickLinks = [
    { label: "Bulking Plans", href: "#bulking" },
    { label: "Cutting Plans", href: "#cutting" },
    { label: "Nutrition Science", href: "#nutrition" },
  ];

  const contactInfo = [
    { icon: Mail, text: "info@thegymjohnson.com" },
    { icon: Phone, text: "+1 (555) 123-4567" },
    { icon: MapPin, text: "Los Angeles, CA" }
  ];

  const socialLinks = [
    { icon: Facebook, href: "#" },
    { icon: Instagram, href: "#" },
    { icon: Youtube, href: "#" },
    { icon: Twitter, href: "#" }
  ];

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId.replace('#', ''));
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <footer id="contact" className="bg-dark-custom text-white py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center mb-6">
              <img 
                src={gymLogo} 
                alt="The Gym by Johnson" 
                className="h-16 w-auto mr-3"
              />
            </div>
            <p className="text-gray-300 mb-6 leading-relaxed">
              Professional nutrition coaching for serious athletes. Transform your body with science-based meal plans designed for your specific goals at The Gym by Johnson.
            </p>
            <div className="flex space-x-4">
              {socialLinks.map((social, index) => (
                <a 
                  key={index}
                  href={social.href} 
                  className="text-gray-300 hover:text-primary-custom transition-colors"
                >
                  <social.icon className="h-6 w-6" />
                </a>
              ))}
            </div>
          </div>
          
          <div>
            <h4 className="text-lg font-bold mb-6">Quick Links</h4>
            <ul className="space-y-3">
              {quickLinks.map((link, index) => (
                <li key={index}>
                  <button 
                    onClick={() => scrollToSection(link.href)}
                    className="text-gray-300 hover:text-primary-custom transition-colors text-left"
                  >
                    {link.label}
                  </button>
                </li>
              ))}
            </ul>
          </div>
          
          <div>
            <h4 className="text-lg font-bold mb-6">Contact Info</h4>
            <ul className="space-y-3">
              {contactInfo.map((contact, index) => (
                <li key={index} className="flex items-center">
                  <contact.icon className="text-primary-custom h-5 w-5 mr-3 flex-shrink-0" />
                  <span className="text-gray-300">{contact.text}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-12 pt-8 text-center">
          <p className="text-gray-300">
            &copy; 2024 The Gym by Johnson. All rights reserved. | Privacy Policy | Terms of Service
          </p>
        </div>
      </div>
    </footer>
  );
}
