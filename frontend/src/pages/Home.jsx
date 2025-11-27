import React from 'react';
import { Link } from 'react-router-dom';
import { Building2, Package, ArrowRight } from 'lucide-react';

const Home = ({ onSchedule }) => {
    return (
        <div className="min-h-screen">
            {/* Hero Section */}
            <div className="bg-gradient-to-br from-emerald-50 via-white to-emerald-50 py-16 md:py-24">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center max-w-3xl mx-auto">
                        <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                            Global Building Systems Index
                        </h1>
                        <p className="text-xl md:text-2xl text-gray-600 mb-8">
                            Discover the world's best regenerative construction technologies
                        </p>
                        <button
                            onClick={() => onSchedule(null)}
                            className="inline-flex items-center gap-2 px-8 py-4 bg-emerald-600 text-white text-lg font-medium rounded-full hover:bg-emerald-700 transition-all shadow-lg hover:shadow-xl"
                        >
                            Schedule Build Consultation
                            <ArrowRight size={20} />
                        </button>
                    </div>
                </div>
            </div>

            {/* Browse Options */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-20">
                <h2 className="text-3xl md:text-4xl font-bold text-center text-gray-900 mb-12">
                    How would you like to explore?
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8">
                    {/* Browse by Vendor */}
                    <Link
                        to="/vendors"
                        className="group relative bg-white rounded-3xl p-8 md:p-12 shadow-sm border-2 border-gray-100 hover:border-emerald-500 hover:shadow-xl transition-all duration-300"
                    >
                        <div className="flex flex-col items-center text-center">
                            <div className="w-20 h-20 md:w-24 md:h-24 bg-emerald-100 rounded-full flex items-center justify-center mb-6 group-hover:bg-emerald-600 transition-colors">
                                <Building2 size={40} className="text-emerald-600 group-hover:text-white transition-colors" />
                            </div>
                            <h3 className="text-2xl md:text-3xl font-bold text-gray-900 mb-4">
                                Browse by Vendor
                            </h3>
                            <p className="text-gray-600 text-lg mb-6">
                                Explore companies and manufacturers pioneering sustainable building solutions
                            </p>
                            <div className="flex items-center gap-2 text-emerald-600 font-medium group-hover:gap-4 transition-all">
                                View Vendors
                                <ArrowRight size={20} />
                            </div>
                        </div>
                    </Link>

                    {/* Browse by Model */}
                    <Link
                        to="/models"
                        className="group relative bg-white rounded-3xl p-8 md:p-12 shadow-sm border-2 border-gray-100 hover:border-emerald-500 hover:shadow-xl transition-all duration-300"
                    >
                        <div className="flex flex-col items-center text-center">
                            <div className="w-20 h-20 md:w-24 md:h-24 bg-emerald-100 rounded-full flex items-center justify-center mb-6 group-hover:bg-emerald-600 transition-colors">
                                <Package size={40} className="text-emerald-600 group-hover:text-white transition-colors" />
                            </div>
                            <h3 className="text-2xl md:text-3xl font-bold text-gray-900 mb-4">
                                Browse by Model
                            </h3>
                            <p className="text-gray-600 text-lg mb-6">
                                Discover specific building products, designs, and construction systems
                            </p>
                            <div className="flex items-center gap-2 text-emerald-600 font-medium group-hover:gap-4 transition-all">
                                View Models
                                <ArrowRight size={20} />
                            </div>
                        </div>
                    </Link>
                </div>
            </div>

            {/* Features Section */}
            <div className="bg-gray-50 py-12 md:py-20">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        <div className="text-center">
                            <div className="text-4xl mb-4">🌱</div>
                            <h3 className="text-xl font-bold text-gray-900 mb-2">Regenerative Focus</h3>
                            <p className="text-gray-600">
                                Curated technologies that restore and regenerate ecosystems
                            </p>
                        </div>
                        <div className="text-center">
                            <div className="text-4xl mb-4">✓</div>
                            <h3 className="text-xl font-bold text-gray-900 mb-2">Certified Partners</h3>
                            <p className="text-gray-600">
                                Verified vendors committed to sustainable practices
                            </p>
                        </div>
                        <div className="text-center">
                            <div className="text-4xl mb-4">🤝</div>
                            <h3 className="text-xl font-bold text-gray-900 mb-2">Expert Guidance</h3>
                            <p className="text-gray-600">
                                Schedule consultations with our building specialists
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Home;
