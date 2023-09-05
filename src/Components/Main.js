import React, { useEffect, useState } from "react";
import { Input } from "@nextui-org/react";
import "./Main.css";
import { Modal, Text, Button, Table } from "@nextui-org/react";
import axios from "axios";

function Main() {
  const [visible, setVisible] = useState(false);
  const handler = () => setVisible(true);
  const [search, setSearch] = useState("");
  const [albumData, setAlbumData] = useState([]);
  const [clickedAlbum, setClickedAlbum] = useState("");

  const closeHandler = () => {
    setVisible(false);
    console.log("closed");
  };

  const searchAlbum = (e) => {
    if (e.key == "Enter") {
      fetch(`//localhost:3001/${search}`)
        .then((response) => response.json())
        .then((data) => setAlbumData(data));
    }
  };

  const Download = () => {
    clickedAlbum.tracks.items.map((track) =>
      axios.get(`http://localhost:3001/download/${search}/${track.name}`)
    );
  };

  const song_link = (track) => {
    axios.get(`http://localhost:3001/download/${search}/${track}`);
  };

  function millisToMinutesAndSeconds(millis) {
    var minutes = Math.floor(millis / 60000);
    var seconds = ((millis % 60000) / 1000).toFixed(0);
    return minutes + ":" + (seconds < 10 ? "0" : "") + seconds;
  }

  return (
    <>
      <div className="search">
        <p>Spotify Downloader</p>
        <Input
          clearable
          labelPlaceholder="Search"
          status="success"
          width="500px"
          onChange={(e) => setSearch(e.target.value)}
          onKeyDown={searchAlbum}
        />
      </div>

      <div className="albums">
        {albumData.map((album) => (
          <>
            <div
              className="album_details"
              onClick={() => {
                setVisible(true);
                setClickedAlbum(album);
              }}
            >
              <img src={album.images[1].url} width="250px" />
              <p>{album.name}</p>
            </div>
          </>
        ))}
      </div>

      {clickedAlbum && (
        <div>
          <Modal
            blur
            aria-labelledby="modal-title"
            open={visible}
            onClose={closeHandler}
            width="1000px"
          >
            <Modal.Header>
              <Text id="modal-title" size={18}>
                {clickedAlbum.name}
              </Text>
            </Modal.Header>
            <Modal.Body>
              <div className="album_info">
                <div className="album_cover">
                  <img src={clickedAlbum.images[1].url} width="300px" />
                  <Button onPress={Download} auto color="success">
                    Download The Album
                  </Button>
                </div>
                <div className="album_tracks">
                  <Table
                    aria-label="Example table with static content"
                    css={{
                      height: 'auto',
                      width: "600px",
                    }}
                  >
                    <Table.Header>
                      <Table.Column>#</Table.Column>
                      <Table.Column>Track Name</Table.Column>
                      <Table.Column>Track Length</Table.Column>
                      <Table.Column>Download</Table.Column>
                    </Table.Header>
                    <Table.Body>
                      {clickedAlbum.tracks.items.map((track, index) => (
                        <Table.Row>
                          <Table.Cell>{index + 1}</Table.Cell>
                          <Table.Cell>{track.name}</Table.Cell>
                          <Table.Cell>
                            {millisToMinutesAndSeconds(track.duration_ms)}
                          </Table.Cell>
                          <Table.Cell>
                            <Button
                              onPress={() => song_link(track.name)}
                              auto
                              color="success"
                            >
                              Download
                            </Button>
                          </Table.Cell>
                        </Table.Row>
                      ))}
                    </Table.Body>
                    <Table.Pagination
                      shadow
                      noMargin
                      align="center"
                      rowsPerPage={5}
                      onPageChange={(page) => console.log({ page })}
                    />
                  </Table>
                </div>
              </div>
            </Modal.Body>
            <Modal.Footer>
              <Button auto flat color="error" onPress={() => setVisible(false)}>
                Close
              </Button>
            </Modal.Footer>
          </Modal>
        </div>
      )}

      {/* <div className="details">
        <img
          src="https://images.squarespace-cdn.com/content/v1/53b6eb62e4b06e0feb2d8e86/1594942678203-T2DZHNP3HW0BDATHQB5Z/SamSpratt_NoPressure_Cover_Final+copy.jpg?format=2500w"
          width="350px"
          height="350px"
        />
        <div>
          <p>Artist Name</p>
          
          <div className="info">
            <p>Album Name</p>
            <p>Track Number</p>
          </div>

          <div className="info">
            <Button auto color="success" onPress={() => setVisible(true)}>
              Show Tracklist
            </Button>
            <Button auto color="success">
              Download
            </Button>
          </div>
        </div>
      </div> */}
    </>
  );
}

export default Main;
