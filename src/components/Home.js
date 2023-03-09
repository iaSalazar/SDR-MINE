import { useNavigate, Link } from "react-router-dom";
import { useContext, useEffect, useState } from "react";
import AuthContext from "../context/AuthProvider";
import axios from "../api/axios";
import { MDBTable, MDBTableHead, MDBTableBody } from "mdb-react-ui-kit";
import useAuth from "../hooks/useAuth";

const Home = () => {
  const { auth } = useAuth();
  console.log(auth?.id);
  const { setAuth } = useContext(AuthContext);
  const navigate = useNavigate();

  const [data, setData] = useState([]);

  const logout = async () => {
    // if used in more components, this should be in context
    // axios to /logout endpoint
    setAuth({});
    navigate("/linkpage");
  };

  useEffect(() => {
    try {
      const response = axios
        .get("/api/recommendations/")
        .then(function (response) {
          console.log(response.data);
          setData(response.data);
        });
      console.log(JSON.stringify(response?.data));
    } catch (error) {}
  }, []);

  return (
    <section className="Home">
      <h1>Home</h1>
      <br />
      <p>You are logged in!</p>
      <br />

      <Link to="/admin">Go to the Admin page</Link>
      <br />
      <div className="flexGrow">
        <button onClick={logout}>Sign Out</button>
      </div>
      <aside>
        <MDBTable bordered striped hover>
          <MDBTableHead>
            <tr>
              <th scope="col">ID</th>
              <th scope="col">NAME</th>
            </tr>
          </MDBTableHead>
          <MDBTableBody>
            {data.map((item, index) => (
              <tr key={index}>
                <td>{item.id}</td>
                <td>{item.username}</td>
              </tr>
            ))}
          </MDBTableBody>
        </MDBTable>
      </aside>
    </section>
  );
};

export default Home;
