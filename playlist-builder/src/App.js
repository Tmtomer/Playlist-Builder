import React from "react";
import { useForm, Controller } from "react-hook-form";
import { Input, RadioGroup, Radio, FormControlLabel, Slider } from "@material-ui/core";

import axios from "axios";
import "./styles.css";


const marks = [
  {
    value: 5,
    label: '5',
  },
  {
    value: 10,
    label: '10',
  },
  {
    value: 15,
    label: '15',
  },
  {
    value: 20,
    label: '20',
  },
  {
    value: 25,
    label: '25',
  },
  {
    value: 30,
    label: '30',
  },
  {
    value: 35,
    label: '35',
  },
  {
    value: 40,
    label: '40',
  },
];



const App = () => {
  const { control, handleSubmit } = useForm();

  const onSubmit = (data) => {
   axios
     .post("/getData", JSON.stringify(data))
     .then(res => console.log(res))
     .catch(err => console.log(err));
 };

  return (
    <form onSubmit={handleSubmit(onSubmit)}
      className="form">
      <label>Song Name</label>
      <Controller
        render={({ field }) => <Input
        className='textBox'
        {...field} />}
        name="songName"
        control={control}
        defaultValue=""
        className="materialUIInput"
      />
      <label>Artist Name</label>
      <Controller
        render={({ field }) => <Input 
        className='textBox'
        {...field} />}
        name="artistName"
        control={control}
        defaultValue=""
        className="materialUIInput"
      />
      <label>Playlist Name</label>
      <Controller
        render={({ field }) => <Input 
        className='textBox'
        {...field} />}
        name="playlistName"
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
                control={<Radio color='primary'/>}
                label="Decrease"
                className='Decrease'
              />
              <FormControlLabel 
                value="1" 
                control={<Radio color='primary'/>} 
                label="Increase" 
                className='Increase'
              />
            </RadioGroup>
          )}

        />
        <label>Playlist Length (songs)</label>
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
            max={40}
            min={5}
            marks={marks}
            step={5}
            color='secondary'
            />
          )}
        />
      <input type="submit" />
    </form>
  );
};


export default App;