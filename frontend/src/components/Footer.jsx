import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faFacebookF,
  faInstagram,
  faWhatsapp,
} from "@fortawesome/free-brands-svg-icons";

function Footer() {
  return (
    <footer className="bg-[#03346E] py-4 px-10 h-[50px]">
      <div className="container mx-auto text-center flex justify-between h-full">
        <p className="h-full">&copy; 2024 AngelCam Web</p>
        <p className="text-sm">All rights reserved.</p>
        <div className="flex justify-center space-x-4">
          <span className="text-gray-400 hover:text-white text-xl">
            <FontAwesomeIcon icon={faFacebookF} />
          </span>
          <span className="text-gray-400 hover:text-white text-xl">
            <FontAwesomeIcon icon={faWhatsapp} />
          </span>
          <span className="text-gray-400 hover:text-white text-xl">
            <FontAwesomeIcon icon={faInstagram} />
          </span>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
