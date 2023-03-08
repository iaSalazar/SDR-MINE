import { useLocation, Navigate, Outlet } from "react-router-dom";
import useAuth from "../hooks/useAuth";

const RequiredAuth = ({ allowedRoles }) => {
  const { auth } = useAuth();
  const location = useLocation();

  //console.log(typeof auth?.roles);
  console.log(auth?.roles);
  const stringRoles = auth?.roles;
  //console.log(auth?.roles?.replace("{", "").repalce("}", "").split(","));
  console.log(stringRoles?.replace('"{', "").replace('}"', "").split(","));
  const stringRolesArray = stringRoles
    ?.replace('"{', "")
    .replace('}"', "")
    .split(",");
  return stringRolesArray?.find((role) => allowedRoles?.includes(role)) ? (
    <Outlet />
  ) : auth?.username ? (
    <Navigate to="/unauthorized" state={{ from: location }} replace />
  ) : (
    <Navigate to="/login" state={{ from: location }} replace />
  );
};

export default RequiredAuth;
