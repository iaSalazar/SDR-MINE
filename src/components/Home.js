import { useNavigate, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "../api/axios";
import { MDBTable, MDBTableHead, MDBTableBody } from "mdb-react-ui-kit";
import useAuth from "../hooks/useAuth";

const Home = () => {
  const { setAuth } = useAuth();
  console.log(setAuth?.id);
  const navigate = useNavigate();

  const [data, setData] = useState([]);
  const [dataItemItem, setDataItemITem] = useState([]);

  const logout = async () => {
    // if used in more components, this should be in context
    // axios to /logout endpoint
    sessionStorage.removeItem("token");
    setAuth({});

    navigate("/login");
  };

  useEffect(() => {
    try {
      console.log(sessionStorage.getItem("token").replaceAll('"', ""));
      const response = axios
        .get("/api/recommendations/", {
          headers: {
            Authorization:
              "Bearer " + sessionStorage.getItem("token").replaceAll('"', ""),
          },
        })
        .then(function (response) {
          console.log(response.data);
          setData(response.data);
        });
      console.log(JSON.stringify(response?.data));
    } catch (error) {}
  }, []);

  useEffect(() => {
    try {
      console.log(sessionStorage.getItem("token").replaceAll('"', ""));
      const response = axios
        .get("/api/recommendations/item-item", {
          headers: {
            Authorization:
              "Bearer " + sessionStorage.getItem("token").replaceAll('"', ""),
          },
        })
        .then(function (response) {
          console.log(response.data);
          setDataItemITem(response.data);
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
              <tr className="tr-hover" key={index}>
                <td>{item.id}</td>
                <td>{item.username}</td>
              </tr>
            ))}
          </MDBTableBody>
        </MDBTable>
      </aside>
      <h2>Item-Item</h2>
      <aside>
        <MDBTable bordered striped hover>
          <MDBTableHead>
            <tr>
              <th scope="col">PREDICTED RANK</th>
              <th scope="col">ARTIST</th>
              <th scope="col">PREDICTED RAITING</th>
            </tr>
          </MDBTableHead>
          <MDBTableBody>
            {dataItemItem?.recomended_movies?.map((item, index) => (
              <tr key={index}>
                <td>{item?.recommended_movies_rank}</td>
                <td>{item?.recomended_movies}</td>
                <td>{item?.raiting}</td>
              </tr>
            ))}
          </MDBTableBody>
        </MDBTable>
      </aside>
    </section>
  );
};

export default Home;
