/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      screens: {
        custom: "1000px",
      },
      colors: {
        "button-bg": "#6EACDA", // Custom button background color
        "card-bg": "#6EACDA",
        "segment-bg": "#E2E2B6",
        white: "#F5EDED",
        grey: "#021526",
        "border-color": "#E5A3B5", // Custom border color
      },
      backgroundImage: {
        "custom-gradient": "red",
      },
    },
  },
  plugins: [],
};
