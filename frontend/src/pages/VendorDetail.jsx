import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { vendorService, modelService } from '../services/api';
import ModelCard from '../components/ModelCard';
import { MapPin, ExternalLink, Calendar } from 'lucide-react';

const VendorDetail = ({ onSchedule }) => {
    const { id } = useParams();
    const [vendor, setVendor] = useState(null);
    const [models, setModels] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadVendorData();
    }, [id]);

    const loadVendorData = async () => {
        try {
            setLoading(true);
            const [vendorData, modelsData] = await Promise.all([
                vendorService.getVendor(id),
                modelService.getAllModels(id)
            ]);
            setVendor(vendorData);
            setModels(modelsData);
        } catch (error) {
            console.error('Failed to load vendor:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleVisitSite = async () => {
        try {
            await vendorService.trackClick(id);
        } catch (error) {
            console.error('Failed to track click:', error);
        }
    };

    if (loading) {
        return (
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <p className="text-center text-gray-500">Loading...</p>
            </div>
        );
    }

    if (!vendor) {
        return (
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <p className="text-center text-gray-500">Vendor not found</p>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            {/* Breadcrumb */}
            <nav className="mb-8">
                <Link to="/vendors" className="text-emerald-600 hover:text-emerald-700">
                    ← Back to Vendors
                </Link>
            </nav>

            {/* Vendor Header */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 mb-8">
                <div className="flex justify-between items-start mb-6">
                    <div>
                        <h1 className="text-4xl font-bold text-gray-900 mb-2">{vendor.partner_name}</h1>
                        <div className="flex items-center gap-4 text-sm text-gray-600">
                            <span className="inline-block bg-emerald-100 text-emerald-800 px-3 py-1 rounded-full font-medium">
                                {vendor.primary_category}
                            </span>
                            {vendor.is_certified && (
                                <span className="inline-block bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full font-medium border border-yellow-200">
                                    Certified Partner
                                </span>
                            )}
                        </div>
                    </div>
                </div>

                <p className="text-gray-700 mb-6">
                    {vendor.metadata?.description || "Leading innovator in sustainable building systems."}
                </p>

                <div className="flex gap-4">
                    {vendor.affiliate_link && (
                        <a
                            href={vendor.affiliate_link}
                            target="_blank"
                            rel="noopener noreferrer"
                            onClick={handleVisitSite}
                            className="flex items-center gap-2 px-6 py-3 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
                        >
                            <ExternalLink size={20} />
                            Visit Website
                        </a>
                    )}
                    <button
                        onClick={() => onSchedule(vendor)}
                        className="flex items-center gap-2 px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium"
                    >
                        <Calendar size={20} />
                        Schedule Consultation
                    </button>
                </div>
            </div>

            {/* Models Section */}
            <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-6">
                    Models by {vendor.partner_name}
                </h2>
                {models.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {models.map(model => (
                            <ModelCard
                                key={model.id}
                                model={model}
                                onSchedule={onSchedule}
                            />
                        ))}
                    </div>
                ) : (
                    <p className="text-gray-500 text-center py-12">
                        No models available for this vendor yet.
                    </p>
                )}
            </div>
        </div>
    );
};

export default VendorDetail;
