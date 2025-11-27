import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { modelService } from '../services/api';
import { Calendar, ExternalLink } from 'lucide-react';

const ModelDetail = ({ onSchedule }) => {
    const { id } = useParams();
    const [model, setModel] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadModel();
    }, [id]);

    const loadModel = async () => {
        try {
            setLoading(true);
            const data = await modelService.getModel(id);
            setModel(data);
        } catch (error) {
            console.error('Failed to load model:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <p className="text-center text-gray-500">Loading...</p>
            </div>
        );
    }

    if (!model) {
        return (
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <p className="text-center text-gray-500">Model not found</p>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            {/* Breadcrumb */}
            <nav className="mb-8">
                <Link to="/models" className="text-emerald-600 hover:text-emerald-700">
                    ← Back to Models
                </Link>
            </nav>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Images */}
                <div>
                    {model.images && model.images.length > 0 ? (
                        <div className="space-y-4">
                            <img
                                src={model.images[0]}
                                alt={model.model_name}
                                className="w-full h-96 object-cover rounded-2xl"
                            />
                            {model.images.length > 1 && (
                                <div className="grid grid-cols-3 gap-4">
                                    {model.images.slice(1, 4).map((img, idx) => (
                                        <img
                                            key={idx}
                                            src={img}
                                            alt={`${model.model_name} ${idx + 2}`}
                                            className="w-full h-24 object-cover rounded-lg"
                                        />
                                    ))}
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="w-full h-96 bg-emerald-100 rounded-2xl flex items-center justify-center">
                            <span className="text-emerald-400 text-2xl font-medium">{model.model_name}</span>
                        </div>
                    )}
                </div>

                {/* Details */}
                <div>
                    <div className="mb-6">
                        <h1 className="text-4xl font-bold text-gray-900 mb-2">{model.model_name}</h1>
                        <Link
                            to={`/vendors/${model.vendor}`}
                            className="text-lg text-emerald-600 hover:text-emerald-700 font-medium"
                        >
                            by {model.vendor_name}
                        </Link>
                        {model.is_featured && (
                            <span className="ml-3 inline-block bg-yellow-100 text-yellow-800 text-sm px-3 py-1 rounded-full font-medium border border-yellow-200">
                                Featured
                            </span>
                        )}
                    </div>

                    {model.price_range && (
                        <div className="mb-6">
                            <p className="text-2xl font-bold text-emerald-600">{model.price_range}</p>
                        </div>
                    )}

                    {model.description && (
                        <div className="mb-6">
                            <h2 className="text-xl font-bold text-gray-900 mb-2">Description</h2>
                            <p className="text-gray-700 whitespace-pre-line">{model.description}</p>
                        </div>
                    )}

                    {model.specifications && Object.keys(model.specifications).length > 0 && (
                        <div className="mb-6">
                            <h2 className="text-xl font-bold text-gray-900 mb-3">Specifications</h2>
                            <dl className="grid grid-cols-2 gap-4">
                                {Object.entries(model.specifications).map(([key, value]) => (
                                    <div key={key} className="border-l-4 border-emerald-500 pl-3">
                                        <dt className="text-sm font-medium text-gray-600">{key}</dt>
                                        <dd className="text-base font-semibold text-gray-900">{value}</dd>
                                    </div>
                                ))}
                            </dl>
                        </div>
                    )}

                    <div className="flex gap-4">
                        {model.vendor_data?.affiliate_link && (
                            <a
                                href={model.vendor_data.affiliate_link}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors font-medium"
                            >
                                <ExternalLink size={20} />
                                Visit Vendor
                            </a>
                        )}
                        <button
                            onClick={() => onSchedule(model)}
                            className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium"
                        >
                            <Calendar size={20} />
                            Schedule Consultation
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ModelDetail;
