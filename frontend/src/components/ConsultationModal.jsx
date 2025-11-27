import React, { useState } from 'react';
import { X } from 'lucide-react';
import { consultationService } from '../services/api';

const ConsultationModal = ({ isOpen, onClose, vendor = null, model = null }) => {
    const [formData, setFormData] = useState({
        email: '',
        phone: '',
        message: ''
    });
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [submitSuccess, setSubmitSuccess] = useState(false);
    const [submitError, setSubmitError] = useState(null);

    if (!isOpen) return null;

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);
        setSubmitError(null);

        try {
            const data = {
                ...formData,
                vendor: vendor?.id || null,
                model: model?.id || null,
            };

            await consultationService.submitRequest(data);
            setSubmitSuccess(true);

            // Reset form after 2 seconds and close
            setTimeout(() => {
                setFormData({ email: '', phone: '', message: '' });
                setSubmitSuccess(false);
                onClose();
            }, 2000);
        } catch (error) {
            setSubmitError('Failed to submit request. Please try again.');
            console.error('Consultation submission error:', error);
        } finally {
            setIsSubmitting(false);
        }
    };

    const getContextMessage = () => {
        if (vendor) return `Interested in ${vendor.partner_name}`;
        if (model) return `Interested in ${model.model_name}`;
        return 'General inquiry';
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl max-w-md w-full p-6 relative">
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 text-gray-400 hover:text-gray-600"
                >
                    <X size={24} />
                </button>

                <h2 className="text-2xl font-bold text-gray-900 mb-2">Schedule Build Consultation</h2>
                <p className="text-sm text-gray-600 mb-6">
                    {getContextMessage()}
                </p>

                {submitSuccess ? (
                    <div className="text-center py-8">
                        <div className="text-emerald-600 text-5xl mb-4">✓</div>
                        <p className="text-lg font-medium text-gray-900">Request Submitted!</p>
                        <p className="text-sm text-gray-600 mt-2">We'll be in touch soon.</p>
                    </div>
                ) : (
                    <form onSubmit={handleSubmit}>
                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Email *
                                </label>
                                <input
                                    type="email"
                                    required
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none"
                                    value={formData.email}
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Phone (optional)
                                </label>
                                <input
                                    type="tel"
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none"
                                    value={formData.phone}
                                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Message *
                                </label>
                                <textarea
                                    required
                                    rows={4}
                                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none resize-none"
                                    value={formData.message}
                                    onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                                    placeholder="Tell us about your project..."
                                />
                            </div>

                            {submitError && (
                                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                                    {submitError}
                                </div>
                            )}

                            <button
                                type="submit"
                                disabled={isSubmitting}
                                className="w-full bg-emerald-600 text-white py-3 rounded-lg font-medium hover:bg-emerald-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {isSubmitting ? 'Submitting...' : 'Submit Request'}
                            </button>
                        </div>
                    </form>
                )}
            </div>
        </div>
    );
};

export default ConsultationModal;
