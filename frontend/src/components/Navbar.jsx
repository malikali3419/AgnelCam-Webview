import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  function handleLogut() {
    localStorage.removeItem("accessToken");
    navigate("/login");
  }
  return (
    <div className="w-full bg-[#03346E] text-white flex justify-between px-10 content-center">
      <div className="h-[50px] w-[210px] flex justify-around items-center">
        {" "}
        <span className=" text-3xl">Angel Cam</span>{" "}
        <span className="text-3xl italic">Web</span>{" "}
      </div>
      <div className="w-[220px] flex  justify-between items-center">
        <Link to={"/cameras"}>
          <button className="px-3 h-[30px] rounded-2xl bg-[#dee2eb] bg-button-bg text-white  w-[100px]">
            Home
          </button>
        </Link>

        <button
          onClick={() => handleLogut()}
          className="px-3 h-[30px] rounded-2xl bg-[#dee2eb] bg-button-bg text-white  w-[100px]"
        >
          Logout
        </button>
      </div>
    </div>
  );
}

export default Navbar;
