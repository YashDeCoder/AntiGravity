import React from 'react';
import { Home, Wallet, PieChart, Info, Settings, LogOut } from 'lucide-react';

const Sidebar = ({ activeTab, setActiveTab }) => {
    const menuItems = [
        { id: 'housing', label: 'Housing Hub', icon: Home },
        { id: 'budget', label: 'Budget Plan', icon: Wallet },
        { id: 'portfolio', label: 'Portfolio', icon: PieChart },
    ];

    return (
        <div className="fixed left-0 top-0 bottom-0 w-64 glass border-r border-border-color p-6 flex flex-col z-50">
            <div className="flex items-center gap-3 mb-12">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent-primary to-accent-secondary flex items-center justify-center shadow-lg shadow-accent-primary/20">
                    <span className="text-xl font-bold italic">AG</span>
                </div>
                <h1 className="text-xl font-bold tracking-tight">AntiGravity</h1>
            </div>

            <nav className="flex-1 flex flex-col gap-2">
                {menuItems.map((item) => (
                    <button
                        key={item.id}
                        onClick={() => setActiveTab(item.id)}
                        className={`flex items-center gap-4 px-4 py-3 rounded-xl transition-all duration-200 group ${activeTab === item.id
                                ? 'bg-accent-primary text-white shadow-lg shadow-accent-primary/25'
                                : 'text-text-secondary hover:bg-bg-tertiary hover:text-text-primary'
                            }`}
                    >
                        <item.icon size={20} className={activeTab === item.id ? 'text-white' : 'text-text-muted group-hover:text-text-primary'} />
                        <span className="font-medium">{item.label}</span>
                    </button>
                ))}
            </nav>

            <div className="mt-auto flex flex-col gap-2 border-t border-border-color pt-6">
                <button className="flex items-center gap-4 px-4 py-3 rounded-xl text-text-secondary hover:bg-bg-tertiary hover:text-text-primary transition-all">
                    <Settings size={20} />
                    <span className="font-medium">Settings</span>
                </button>
                <button className="flex items-center gap-4 px-4 py-3 rounded-xl text-text-secondary hover:bg-red-500/10 hover:text-red-400 transition-all">
                    <LogOut size={20} />
                    <span className="font-medium">Sign Out</span>
                </button>
            </div>
        </div>
    );
};

export default Sidebar;
