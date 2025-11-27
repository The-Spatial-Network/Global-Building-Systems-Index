/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                terralux: {
                    50: '#f2fcf5',
                    100: '#e1f8e8',
                    200: '#c3eed2',
                    300: '#94deb3',
                    400: '#5dc58f',
                    500: '#38a76e',
                    600: '#288656',
                    700: '#226b46',
                    800: '#1e553a',
                    900: '#194631',
                    950: '#0d271c',
                },
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
