import React from 'react';
import { Calendar, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

const ModelCard = ({ model, onSchedule }) => {
    const firstImage = model.images && model.images.length > 0 ? model.images[0] : null;

    return (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-lg hover:border-emerald-200 transition-all duration-300">
            {/* Image */}
            <Link to={`/models/${model.id}`} className="block">
                <div className="h-48 bg-gradient-to-br from-emerald-100 to-emerald-50 flex items-center justify-center relative overflow-hidden">
                    {firstImage ? (
                        <img src={firstImage} alt={model.model_name} className="w-full h-full object-cover" />
                    ) : (
                        <span className="text-emerald-400 font-medium text-lg">{model.model_name}</span>
                    )}
                    {model.is_featured && (
                        <span className="absolute top-3 right-3 bg-yellow-400 text-yellow-900 text-xs px-2.5 py-1 rounded-full font-medium shadow-sm">
                            ⭐ Featured
                        </span>
                    )}
                </div>
            </Link>

            {/* Content */}
            <div className="p-5">
                <Link to={`/models/${model.id}`}>
                    <h3 className="text-xl font-bold text-gray-900 mb-1 hover:text-emerald-600 transition-colors">
                        {model.model_name}
                    </h3>
                </Link>
                <Link
                    to={`/vendors/${model.vendor}`}
                    className="text-sm text-emerald-600 hover:text-emerald-700 font-medium mb-3 inline-block"
                >
                    by {model.vendor_name}
                </Link>

                {model.price_range && (
                    <p className="text-base font-semibold text-gray-900 mb-4">{model.price_range}</p>
                )}

                {/* Actions */}
                <div className="flex gap-2">
                    <Link
                        to={`/models/${model.id}`}
                        className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-gray-50 border border-gray-200 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors text-sm font-medium"
                    >
                        Details
                        <ArrowRight size={14} />
                    </Link>
                    <button
                        onClick={() => onSchedule(model)}
                        className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors text-sm font-medium"
                    >
                        <Calendar size={14} />
                        Consult
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ModelCard;
