import { useNavigate, Link } from "react-router-dom";
import { useEffect, useState, useRef } from "react";
import axios from "../api/axios";
import { MDBTable, MDBTableHead, MDBTableBody } from "mdb-react-ui-kit";
import useAuth from "../hooks/useAuth";

const Home = () => {
  const { auth, setAuth } = useAuth();
  console.log(auth?.id);
  const username = useRef(auth.username);
  const navigate = useNavigate();

  const [dataItemItem, setDataItemITem] = useState([]);

  const [dataGeneric, setDataGeneric] = useState([]);

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
      const response = async () =>
        await axios
          .get("/api/recommendations/generic", {
            headers: {
              Authorization:
                "Bearer " + sessionStorage.getItem("token").replaceAll('"', ""),
            },
          })
          .then(function (response) {
            console.log(response.data);
            setDataGeneric(response.data);
          });
      console.log(JSON.stringify(response?.data));
      response();
    } catch (error) {}
  }, []);

  useEffect(() => {
    try {
      console.log(sessionStorage.getItem("token").replaceAll('"', ""));
      const response = async () =>
        await axios
          .post("/api/recommendations/item-item", {
            headers: {
              "Content-Type": "application/json",
              Authorization:
                "Bearer " + sessionStorage.getItem("token").replaceAll('"', ""),
            },
            body: { username: username.current },
          })
          .then(function (response) {
            console.log(response.data);
            setDataItemITem(response.data);
          });
      console.log(JSON.stringify(response?.data));
      response();
    } catch (error) {}
  }, []);

  return (
    <section className="Home">
      <h1>Home</h1>
      <br />
      <p>You are logged in as {username.current}!</p>
      <br />

      <Link to="/admin">Go to the Admin page</Link>
      <Link to="/rate">rate some artist</Link>
      <br />
      <div className="flexGrow">
        <button onClick={logout}>Sign Out</button>
      </div>

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
            {dataItemItem?.recomended_artists?.map((item, index) => (
              <tr key={index}>
                <td>{item?.recommended_artists_rank}</td>
                <td>{item?.recomended_artists}</td>
                <td>{item?.raiting}</td>
              </tr>
            ))}
          </MDBTableBody>
        </MDBTable>
      </aside>
      <h2>Generic</h2>
      <aside>
        <MDBTable bordered striped hover>
          <MDBTableHead>
            <tr>
              <th scope="col">ARTIST NAME</th>
              <th scope="col">MEAN RATING</th>
              <th scope="col">NUMBER OF RATINGS</th>
            </tr>
          </MDBTableHead>
          <MDBTableBody>
            {dataGeneric?.map((item, index) => (
              <tr key={index}>
                <td>{item?.artist_name}</td>
                <td>{item?.mean_rating}</td>
                <td>{item?.number_of_ratings}</td>
              </tr>
            ))}
          </MDBTableBody>
        </MDBTable>
      </aside>
      <aside>
        <h2>History</h2>
        <MDBTable bordered striped hover>
          <MDBTableBody>
            {dataItemItem?.listened_artist?.map((item, index) => (
              <tr key={index}>
                <td>{item.rated_artist}</td>
                <td>{item.rating}</td>
              </tr>
            ))}
          </MDBTableBody>
        </MDBTable>
      </aside>
    </section>
  );
};

export default Home;
