function EventButtons({ children, className, onClick, ...props }) {
  return (
    <div>
      <button
        onClick={onClick}
        className={` px-3  min-w-[40px] min-h-[30px] me-2 rounded bg-gray text-white font-semibold hover:bg-gray-700 transition ${className}`}
        {...props}
      >
        {children}
      </button>
    </div>
  );
}

export default EventButtons;
