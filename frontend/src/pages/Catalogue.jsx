import React, { useState, useEffect } from 'react';
import VendorCard from '../components/VendorCard';
import { Search, Filter } from 'lucide-react';
import { vendorService } from '../services/api';

// Mock data as fallback
const MOCK_VENDORS = [
    {
        id: 1,
        partner_name: "Pacific Domes",
        primary_category: "DOMES",
        is_certified: true,
        consultation_enabled: true,
        affiliate_link: "https://pacificdomes.com/?ref=terralux",
        metadata: { description: "Geodesic domes for eco-living and events." }
    },
    {
        id: 2,
        partner_name: "ICON Build",
        primary_category: "3D_PRINT",
        is_certified: true,
        consultation_enabled: true,
        affiliate_link: "https://iconbuild.com",
        metadata: { description: "Advanced 3D construction technologies." }
    },
    {
        id: 3,
        partner_name: "Cob Cottage Company",
        primary_category: "NATURAL",
        is_certified: false,
        consultation_enabled: false,
        affiliate_link: "https://cobcottage.com",
        metadata: { description: "Traditional cob building workshops and designs." }
    }
];

const Catalogue = () => {
    const [vendors, setVendors] = useState(MOCK_VENDORS);
    const [searchTerm, setSearchTerm] = useState("");
    const [selectedCategory, setSelectedCategory] = useState("ALL");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadVendors();
    }, []);

    const loadVendors = async () => {
        try {
            setLoading(true);
            const data = await vendorService.getAllVendors();
            if (data && data.length > 0) {
                setVendors(data);
            }
            setError(null);
        } catch (err) {
            console.error('Failed to load vendors from API, using mock data:', err);
            setError('Using demo data (backend not connected)');
            // Keep using mock data
        } finally {
            setLoading(false);
        }
    };

    const handleSchedule = (vendor) => {
        // Integration with Cal.com would go here
        console.log("Scheduling for:", vendor.partner_name);
        alert(`Opening scheduling for ${vendor.partner_name}`);
    };

    const handleVisitSite = async (vendor) => {
        try {
            await vendorService.trackClick(vendor.id);
            console.log('Click tracked for:', vendor.partner_name);
        } catch (err) {
            console.error('Failed to track click:', err);
        }
        // The link will open naturally via the anchor tag
    };

    const filteredVendors = vendors.filter(vendor => {
        const matchesSearch = vendor.partner_name.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesCategory = selectedCategory === "ALL" || vendor.primary_category === selectedCategory;
        return matchesSearch && matchesCategory;
    });

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
            <div className="mb-8 md:mb-12">
                <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">Vendor Catalogue</h1>
                <p className="text-lg text-gray-600">
                    Explore companies pioneering sustainable building solutions
                </p>
                {error && (
                    <p className="text-sm text-amber-600 mt-2">
                        ⚠️ {error}
                    </p>
                )}
            </div>

            <div className="flex flex-col sm:flex-row gap-3 mb-6 md:mb-8">
                <div className="relative flex-1">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                    <input
                        type="text"
                        placeholder="Search vendors..."
                        className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <div className="relative sm:min-w-[200px]">
                    <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                    <select
                        className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all appearance-none bg-white"
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                    >
                        <option value="ALL">All Categories</option>
                        <option value="PREFAB">Prefab & Modular</option>
                        <option value="NATURAL">Natural & Earthen</option>
                        <option value="DOMES">Domes & Shells</option>
                        <option value="3D_PRINT">3D Printed</option>
                    </select>
                </div>
            </div>

            {loading ? (
                <div className="text-center py-12">
                    <p className="text-gray-500">Loading vendors...</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
                    {filteredVendors.map(vendor => (
                        <VendorCard
                            key={vendor.id}
                            vendor={vendor}
                            onSchedule={handleSchedule}
                            onVisitSite={() => handleVisitSite(vendor)}
                        />
                    ))}
                </div>
            )}
        </div>
    );
};

export default Catalogue;
