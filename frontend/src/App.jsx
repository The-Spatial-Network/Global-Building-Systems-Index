import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Catalogue from './pages/Catalogue';
import VendorDetail from './pages/VendorDetail';
import ModelCatalogue from './pages/ModelCatalogue';
import ModelDetail from './pages/ModelDetail';
import ConsultationModal from './components/ConsultationModal';
import { Calendar, Menu, X } from 'lucide-react';

function App() {
  const [showConsultationModal, setShowConsultationModal] = useState(false);
  const [consultationContext, setConsultationContext] = useState({ vendor: null, model: null });
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleSchedule = (item) => {
    // Determine if it's a vendor or model based on properties
    if (item?.partner_name) {
      // It's a vendor
      setConsultationContext({ vendor: item, model: null });
    } else if (item?.model_name) {
      // It's a model
      setConsultationContext({ vendor: null, model: item });
    } else {
      // General consultation
      setConsultationContext({ vendor: null, model: null });
    }
    setShowConsultationModal(true);
  };

  const handleHeaderConsultation = () => {
    setConsultationContext({ vendor: null, model: null });
    setShowConsultationModal(true);
  };

  const closeMobileMenu = () => {
    setMobileMenuOpen(false);
  };

  return (
    <Router>
      <div className="min-h-screen bg-white">
        <nav className="bg-white border-b border-gray-100 sticky top-0 z-50 shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16 items-center">
              {/* Logo */}
              <Link to="/" className="text-2xl font-bold text-emerald-600" onClick={closeMobileMenu}>
                TerraLux
              </Link>

              {/* Desktop Navigation */}
              <div className="hidden md:flex items-center space-x-8">
                <Link to="/vendors" className="text-gray-700 hover:text-emerald-600 font-medium transition-colors">
                  Vendors
                </Link>
                <Link to="/models" className="text-gray-700 hover:text-emerald-600 font-medium transition-colors">
                  Models
                </Link>
                <button
                  onClick={handleHeaderConsultation}
                  className="flex items-center gap-2 px-5 py-2.5 bg-emerald-600 text-white rounded-full hover:bg-emerald-700 font-medium transition-all shadow-md hover:shadow-lg"
                >
                  <Calendar size={18} />
                  Schedule Consultation
                </button>
              </div>

              {/* Mobile Menu Button */}
              <div className="md:hidden flex items-center gap-3">
                <button
                  onClick={handleHeaderConsultation}
                  className="p-2 bg-emerald-600 text-white rounded-full hover:bg-emerald-700 transition-colors"
                >
                  <Calendar size={20} />
                </button>
                <button
                  onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                  className="p-2 text-gray-700 hover:text-emerald-600 transition-colors"
                >
                  {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
                </button>
              </div>
            </div>
          </div>

          {/* Mobile Menu */}
          {mobileMenuOpen && (
            <div className="md:hidden border-t border-gray-100 bg-white">
              <div className="px-4 py-4 space-y-3">
                <Link
                  to="/vendors"
                  onClick={closeMobileMenu}
                  className="block px-4 py-3 text-gray-700 hover:bg-emerald-50 hover:text-emerald-600 rounded-lg font-medium transition-colors"
                >
                  Browse Vendors
                </Link>
                <Link
                  to="/models"
                  onClick={closeMobileMenu}
                  className="block px-4 py-3 text-gray-700 hover:bg-emerald-50 hover:text-emerald-600 rounded-lg font-medium transition-colors"
                >
                  Browse Models
                </Link>
                <button
                  onClick={() => {
                    handleHeaderConsultation();
                    closeMobileMenu();
                  }}
                  className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 font-medium transition-colors"
                >
                  <Calendar size={18} />
                  Schedule Consultation
                </button>
              </div>
            </div>
          )}
        </nav>

        <main>
          <Routes>
            <Route path="/" element={<Home onSchedule={handleSchedule} />} />
            <Route path="/vendors" element={<Catalogue onSchedule={handleSchedule} />} />
            <Route path="/vendors/:id" element={<VendorDetail onSchedule={handleSchedule} />} />
            <Route path="/models" element={<ModelCatalogue onSchedule={handleSchedule} />} />
            <Route path="/models/:id" element={<ModelDetail onSchedule={handleSchedule} />} />
          </Routes>
        </main>

        <ConsultationModal
          isOpen={showConsultationModal}
          onClose={() => setShowConsultationModal(false)}
          vendor={consultationContext.vendor}
          model={consultationContext.model}
        />
      </div>
    </Router>
  );
}

export default App;
