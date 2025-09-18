import React from 'react';
import { Facebook, Twitter, Instagram, Youtube, Mail, Phone, MapPin } from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Separator } from './ui/separator';

const Footer = () => {
  const footerLinks = {
    'Company': ['About Us', 'Careers', 'Press', 'Investor Relations'],
    'Support': ['Help Center', 'Terms of Service', 'Privacy Policy', 'Contact Us'],
    'Features': ['Movies', 'TV Shows', 'Live Sports', 'Documentaries'],
    'Devices': ['Smart TV', 'Mobile App', 'Desktop', 'Game Consoles']
  };

  const socialLinks = [
    { icon: Facebook, name: 'Facebook', href: '#' },
    { icon: Twitter, name: 'Twitter', href: '#' },
    { icon: Instagram, name: 'Instagram', href: '#' },
    { icon: Youtube, name: 'YouTube', href: '#' }
  ];

  return (
    <footer className="bg-gray-950 border-t border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Newsletter Section */}
        <div className="mb-12">
          <div className="max-w-md mx-auto text-center">
            <h3 className="text-xl font-semibold text-white mb-4">Stay Updated</h3>
            <p className="text-gray-400 mb-6">Get notified about new movies, shows and exclusive content.</p>
            <div className="flex gap-2">
              <Input
                type="email"
                placeholder="Enter your email"
                className="bg-gray-900 border-gray-700 text-white placeholder-gray-400 focus:border-red-500"
              />
              <Button className="bg-red-600 hover:bg-red-700 text-white">
                <Mail className="w-4 h-4 mr-2" />
                Subscribe
              </Button>
            </div>
          </div>
        </div>

        <Separator className="bg-gray-800 mb-12" />

        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 mb-8">
          {/* Brand Section */}
          <div className="lg:col-span-1">
            <h2 className="text-2xl font-bold text-red-500 mb-4">StreamFlix</h2>
            <p className="text-gray-400 mb-6">
              Your ultimate destination for movies, TV shows, and live sports. Stream unlimited entertainment anytime, anywhere.
            </p>
            
            {/* Social Links */}
            <div className="flex space-x-4">
              {socialLinks.map(({ icon: Icon, name, href }) => (
                <Button
                  key={name}
                  variant="ghost"
                  size="sm"
                  className="text-gray-400 hover:text-white p-2"
                  asChild
                >
                  <a href={href} aria-label={name}>
                    <Icon className="w-5 h-5" />
                  </a>
                </Button>
              ))}
            </div>
          </div>

          {/* Footer Links */}
          {Object.entries(footerLinks).map(([category, links]) => (
            <div key={category}>
              <h4 className="font-semibold text-white mb-4">{category}</h4>
              <ul className="space-y-3">
                {links.map((link) => (
                  <li key={link}>
                    <a
                      href="#"
                      className="text-gray-400 hover:text-white transition-colors duration-200"
                    >
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <Separator className="bg-gray-800 mb-8" />

        {/* Contact Information */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="flex items-center space-x-3 text-gray-400">
            <Phone className="w-5 h-5 text-red-500" />
            <span>+1 (555) 123-4567</span>
          </div>
          <div className="flex items-center space-x-3 text-gray-400">
            <Mail className="w-5 h-5 text-red-500" />
            <span>support@streamflix.com</span>
          </div>
          <div className="flex items-center space-x-3 text-gray-400">
            <MapPin className="w-5 h-5 text-red-500" />
            <span>Los Angeles, CA 90210</span>
          </div>
        </div>

        <Separator className="bg-gray-800 mb-6" />

        {/* Bottom Section */}
        <div className="flex flex-col md:flex-row justify-between items-center text-gray-400 text-sm">
          <p>&copy; 2025 StreamFlix. All rights reserved.</p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <a href="#" className="hover:text-white transition-colors duration-200">
              Privacy Policy
            </a>
            <a href="#" className="hover:text-white transition-colors duration-200">
              Terms of Service
            </a>
            <a href="#" className="hover:text-white transition-colors duration-200">
              Cookie Policy
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;