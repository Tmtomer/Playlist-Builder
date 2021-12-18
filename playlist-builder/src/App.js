import React from "react";
import ReactDOM from "react-dom";
import Select from "react-select";
import Box from '@mui/material/Box';
import { useForm, Controller } from "react-hook-form";
import { Input, RadioGroup, Radio, FormControlLabel, Slider } from "@material-ui/core";

import "./styles.css";


const marks = [
  {
    value: 15,
    label: '15 mins',
  },
  {
    value: 30,
    label: '30 mins',
  },
  {
    value: 45,
    label: '45 mins',
  },
  {
    value: 60,
    label: '60 mins',
  },
  {
    value: 75,
    label: '75 mins',
  },
  {
    value: 90,
    label: '90 mins',
  },
  {
    value: 105,
    label: '100 mins',
  },
  {
    value: 120,
    label: '120 mins',
  },
];


const App = () => {
  const { control, handleSubmit } = useForm();

  const onSubmit = (data) => {
    alert(JSON.stringify(data));
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <label>Song Name</label>
      <Controller
        render={({ field }) => <Input {...field} />}
        name="songName"
        control={control}
        defaultValue=""
        className="materialUIInput"
      />
      <label>Tempo</label>
      <Controller
        name="tempo"
        control={control}
        render={({ field }) => (
          <RadioGroup aria-label="tempo" {...field}>
              <FormControlLabel
                value="0"
                control={<Radio />}
                label="Decrease"
              />
              <FormControlLabel 
                value="1" 
                control={<Radio />} 
                label="Increase" 
              />
            </RadioGroup>
          )}

        />
        <label>Playlist Length (mins)</label>
        <Controller
          name="length"
          control={control}
          defaultValue={15}
          render={({ field }) => (
            <Slider
              {...field}
              onChange={(_, value) => {
                field.onChange(value);
              }}
              valueLabelDisplay="auto"
              max={120}
              min={15}
              marks={marks}
              step={15}
            />
          )}
        />
      <input type="submit" />
    </form>
  );
};


export default App;