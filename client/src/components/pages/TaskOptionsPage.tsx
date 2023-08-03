// import "./TaskOptionsPage.css";

import Button from "@mui/material/Button";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormGroup from "@mui/material/FormGroup";
import { useContext } from "react";
import { useNavigate } from "react-router";
import { appApiUrl } from "utils";
import { AppContext } from "utils/AppContext";

export default function TaskOptionsPage() {
  const navigate = useNavigate();
  const { reloadActiveTask } = useContext(AppContext);

  async function handleSubmit(e) {
    // Prevent the browser from reloading the page
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    const response = await fetch(appApiUrl("/api/task"), {
      method: "post",
      body: formData,
    });

    if (response.ok) {
      reloadActiveTask();
      navigate("/active_task");
    }
  }
  return (
    <>
      <form onSubmit={handleSubmit}>
        <p>
          <FormGroup>
            <FormControlLabel
              control={
                <Checkbox
                  defaultChecked
                  name="refresh_media_items"
                  value="true"
                />
              }
              label="Refresh media items"
            />
          </FormGroup>
        </p>
        <p>
          <Button type="submit" variant="contained">
            Start
          </Button>
        </p>
      </form>
    </>
  );
}