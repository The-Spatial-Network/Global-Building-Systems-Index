import React, { useState, useEffect } from 'react';
import ModelCard from '../components/ModelCard';
import { Search, Filter } from 'lucide-react';
import { modelService } from '../services/api';

const ModelCatalogue = ({ onSchedule }) => {
    const [models, setModels] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [selectedVendor, setSelectedVendor] = useState("ALL");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadModels();
    }, []);

    const loadModels = async () => {
        try {
            setLoading(true);
            const data = await modelService.getAllModels();
            setModels(data);
            setError(null);
        } catch (err) {
            console.error('Failed to load models:', err);
            setError('Failed to load models');
        } finally {
            setLoading(false);
        }
    };

    const filteredModels = models.filter(model => {
        const matchesSearch = model.model_name.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesVendor = selectedVendor === "ALL" || model.vendor === parseInt(selectedVendor);
        return matchesSearch && matchesVendor;
    });

    // Get unique vendors for filter
    const vendors = [...new Map(models.map(m => [m.vendor, { id: m.vendor, name: m.vendor_name }])).values()];

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12">
            <div className="mb-8 md:mb-12">
                <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">Building Models</h1>
                <p className="text-lg text-gray-600">
                    Explore specific building products and designs
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
                        placeholder="Search models..."
                        className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <div className="relative sm:min-w-[200px]">
                    <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                    <select
                        className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all appearance-none bg-white"
                        value={selectedVendor}
                        onChange={(e) => setSelectedVendor(e.target.value)}
                    >
                        <option value="ALL">All Vendors</option>
                        {vendors.map(vendor => (
                            <option key={vendor.id} value={vendor.id}>{vendor.name}</option>
                        ))}
                    </select>
                </div>
            </div>

            {loading ? (
                <div className="text-center py-12">
                    <p className="text-gray-500">Loading models...</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
                    {filteredModels.map(model => (
                        <ModelCard
                            key={model.id}
                            model={model}
                            onSchedule={onSchedule}
                        />
                    ))}
                </div>
            )}
        </div>
    );
};

export default ModelCatalogue;
