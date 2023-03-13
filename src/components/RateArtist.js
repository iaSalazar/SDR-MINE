import { useEffect, useState, useRef } from "react";
import axios from "../api/axios";
import { Link } from "react-router-dom";

const RateArtist = () => {
  const [artistData, setArtistData] = useState([]);
  const [optionValue, setOptionValue] = useState("");
  const [artistRating, setArtistRating] = useState(0);
  const RATE_URL = "/api/rate";

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(JSON.stringify({ artist: optionValue, rating: artistRating }));
    try {
      const response = await axios.post(
        RATE_URL,
        JSON.stringify({ artist: optionValue, rating: artistRating }),
        {
          headers: { "Content-Type": "application/json" },

          // withCredentials: true,
        }
      );
      console.log(response.data);
      console.log("______________----_____");
      console.log(response.acces_token);
      console.log("______________----_____");
      console.log(JSON.stringify(response.status));
      console.log(JSON.stringify(response));
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    try {
      console.log(sessionStorage.getItem("token").replaceAll('"', ""));
      const response = async () =>
        await axios
          .get("/api/artists", {
            headers: {
              Authorization:
                "Bearer " + sessionStorage.getItem("token").replaceAll('"', ""),
            },
          })
          .then(function (response) {
            console.log(response.data);
            setArtistData(response.data);
          });
      console.log(JSON.stringify(response?.data));
      response();
    } catch (error) {}
  }, []);

  return (
    <div>
      <div className="flexGrow">
        <Link to="/">Home</Link>
      </div>
      <section>
        return{" "}
        <div className="drop-down">
          <p>Rate some artist</p>
          <form onSubmit={handleSubmit}>
            <select required onChange={(e) => setOptionValue(e.target.value)}>
              <option value="">--Please choose an artist--</option>
              {artistData?.map((artist, index) => {
                return (
                  <option key={index} value={artist.name}>
                    {artist.name}
                  </option>
                );
              })}
            </select>
            <input
              type="number"
              step="0.1"
              id="rating"
              required
              onChange={(e) => setArtistRating(e.target.value)}
            />
            <button>Rate</button>
          </form>
        </div>
        <div>{optionValue}</div>
        <div>{artistRating}</div>
      </section>
    </div>
  );
};

export default RateArtist;
