import React from 'react';
import { ExternalLink, Calendar, MapPin } from 'lucide-react';
import { Link } from 'react-router-dom';

const VendorCard = ({ vendor, onSchedule, onVisitSite }) => {
    return (
        <Link
            to={`/vendors/${vendor.id}`}
            className="block bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg hover:border-emerald-200 transition-all duration-300"
        >
            {/* Header with gradient */}
            <div className="h-32 bg-gradient-to-br from-emerald-500 to-emerald-600 flex items-center justify-center relative p-6">
                <h3 className="text-2xl font-bold text-white text-center">{vendor.partner_name}</h3>
                {vendor.is_certified && (
                    <span className="absolute top-3 right-3 bg-yellow-400 text-yellow-900 text-xs px-2 py-1 rounded-full font-medium shadow-sm">
                        ✓ Certified
                    </span>
                )}
            </div>

            {/* Content */}
            <div className="p-5">
                <div className="flex items-center gap-2 mb-3">
                    <span className="inline-block bg-emerald-50 text-emerald-700 text-sm px-3 py-1 rounded-full font-medium">
                        {vendor.primary_category}
                    </span>
                    {vendor.heal_alignment === 'HIGH' && (
                        <span className="text-emerald-600 text-sm font-medium">🌱 High Impact</span>
                    )}
                </div>

                <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                    {vendor.metadata?.description || "Leading innovator in sustainable building systems."}
                </p>

                {/* Quick Actions */}
                <div className="flex gap-2">
                    {vendor.affiliate_link && (
                        <button
                            onClick={(e) => {
                                e.preventDefault();
                                onVisitSite();
                                window.open(vendor.affiliate_link, '_blank');
                            }}
                            className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2 bg-gray-50 border border-gray-200 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors text-sm font-medium"
                        >
                            <ExternalLink size={14} />
                            <span className="hidden sm:inline">Visit</span>
                        </button>
                    )}
                    {vendor.consultation_enabled && (
                        <button
                            onClick={(e) => {
                                e.preventDefault();
                                onSchedule(vendor);
                            }}
                            className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors text-sm font-medium"
                        >
                            <Calendar size={14} />
                            <span className="hidden sm:inline">Schedule</span>
                        </button>
                    )}
                </div>
            </div>
        </Link>
    );
};

export default VendorCard;
