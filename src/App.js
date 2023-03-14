import Register from "./components/Register";
import Login from "./components/Login";
import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Home from "./components/Home";
import Admin from "./components/Admin";
import RequiredAuth from "./components/RequiredAuth";
import Unauthorized from "./components/Unauthorized";
import RateArtist from "./components/RateArtist";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        {/* public routes */}

        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
        <Route path="unauthorized" element={<Unauthorized />} />
        {/* protected routes */}
        <Route element={<RequiredAuth allowedRoles={["admin"]} />}>
          <Route path="Admin" element={<Admin />} />
        </Route>
        <Route element={<RequiredAuth allowedRoles={["user"]} />}>
          <Route path="/" element={<Home />} />
        </Route>
        <Route element={<RequiredAuth allowedRoles={["user"]} />}>
          <Route path="/rate" element={<RateArtist />} />
        </Route>
        {/* catch all*/}
      </Route>
    </Routes>
  );
}

export default App;
