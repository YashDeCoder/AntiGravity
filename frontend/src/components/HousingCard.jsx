import React from 'react';
import { Home, MapPin, Clock, ExternalLink, TrendingUp } from 'lucide-react';

const HousingCard = ({ house }) => {
    const { title, price, location, travel_data, source, link } = house;

    return (
        <div className="glass rounded-2xl p-4 card-hover overflow-hidden flex flex-col gap-4 border border-border-color">
            <div className="relative h-48 -mx-4 -mt-4 bg-tertiary/50 overflow-hidden group">
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                <div className="absolute top-3 left-3 bg-accent-primary/80 backdrop-blur-md px-2 py-1 rounded-lg text-xs font-semibold text-white uppercase tracking-wider">
                    {source}
                </div>
                <div className="absolute bottom-3 left-3 right-3 flex items-end justify-between">
                    <div className="flex flex-col">
                        <span className="text-2xl font-bold">€{price.toLocaleString()}</span>
                        <span className="text-xs text-text-secondary">per maand</span>
                    </div>
                </div>
            </div>

            <div className="flex flex-col gap-2">
                <h3 className="text-lg font-semibold truncate text-text-primary">{title}</h3>
                <div className="flex items-center gap-1 text-sm text-text-secondary">
                    <MapPin size={14} className="text-accent-primary" />
                    <span className="truncate">{location}</span>
                </div>
            </div>

            {travel_data && (
                <div className="grid grid-cols-2 gap-2 mt-auto">
                    <div className="bg-bg-tertiary/50 rounded-xl p-2 flex items-center gap-2">
                        <Clock size={16} className="text-accent-secondary" />
                        <div className="flex flex-col">
                            <span className="text-xs text-text-muted">Travel</span>
                            <span className="text-sm font-medium">{travel_data.duration_mins} min</span>
                        </div>
                    </div>
                    <div className="bg-bg-tertiary/50 rounded-xl p-2 flex items-center gap-2">
                        <TrendingUp size={16} className="text-accent-success" />
                        <div className="flex flex-col">
                            <span className="text-xs text-text-muted">Dist.</span>
                            <span className="text-sm font-medium">{travel_data.distance_km} km</span>
                        </div>
                    </div>
                </div>
            )}

            <a
                href={link}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-2 w-full flex items-center justify-center gap-2 py-2.5 rounded-xl bg-accent-primary hover:bg-accent-secondary transition-colors font-medium text-white text-sm"
            >
                View Detail <ExternalLink size={14} />
            </a>
        </div>
    );
};

export default HousingCard;
