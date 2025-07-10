import Navigation from "@/components/navigation";
import HeroSection from "@/components/hero-section";
import StatsSection from "@/components/stats-section";
import BulkingSection from "@/components/bulking-section";
import CuttingSection from "@/components/cutting-section";
import NutritionSection from "@/components/nutrition-section";
import CTASection from "@/components/cta-section";
import Footer from "@/components/footer";

export default function Home() {
  return (
    <div className="min-h-screen">
      <Navigation />
      <HeroSection />
      <StatsSection />
      <BulkingSection />
      <CuttingSection />
      <NutritionSection />
      <CTASection />
      <Footer />
    </div>
  );
}
