import React from "react";
import { Input } from "@nextui-org/react";
import "./Main.css";
import { Modal, useModal, Text, Button, Pagination } from "@nextui-org/react";

function Main() {
  const [visible, setVisible] = React.useState(false);
  const handler = () => setVisible(true);
  const closeHandler = () => {
    setVisible(false);
    console.log("closed");
  };
  return (
    <>
      <div className="search">
        <Input
          clearable
          underlined
          labelPlaceholder="Search"
          status="success"
          width="500px"
        />
      </div>

      <div className="details">
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
      </div>

      <div>
        <Modal
          closeButton
          blur
          aria-labelledby="modal-title"
          open={visible}
          onClose={closeHandler}
        >
          <Modal.Header>
            <Text id="modal-title" size={18}>
              Modal with a lot of content
            </Text>
          </Modal.Header>
          <Modal.Body>
            <Text id="modal-description">
              <Pagination color="success" total={20} initialPage={1} />
            </Text>
          </Modal.Body>
          <Modal.Footer>
            <Button auto flat color="error" onPress={() => setVisible(false)}>
              Close
            </Button>
          </Modal.Footer>
        </Modal>
      </div>
    </>
  );
}

export default Main;
