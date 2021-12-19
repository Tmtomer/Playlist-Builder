import React from "react";
import { useForm, Controller } from "react-hook-form";
import { Input, RadioGroup, Radio, FormControlLabel, Slider, Toolbar} from "@material-ui/core";
import AppBar from '@material-ui/core/AppBar';
import {Link} from 'react-router-dom';
import Box from '@mui/material/Box';
import Image from 'material-ui-image';

import axios from "axios";
import "./styles.css";
import Typography from "@material-ui/core/Typography";



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
     .then(res => alert("Checkout SeekBeats official spotify account for your playlist!"))
     .catch(err => console.log(err));
 };

  return (
   <div>
      <AppBar>
         <Toolbar>
            <img
               className='Image'
               src='http://localhost:3000/SeekBeats.png'
            />
            <Typography variant="h6" className='title'>
               SeekBeats Playlist-Builder
            </Typography>
         </Toolbar>
      </AppBar>
      <form onSubmit={handleSubmit(onSubmit)}
         className="form">
         <label>Song Name</label>
         <section>
            <Controller
            render={({ field }) => <Input {...field} />}
            name="songName"
            control={control}
            defaultValue=""
            className="materialUIInput"
            />
         </section>
         <label>Artist Name</label>
         <section>
            <Controller
            render={({ field }) => <Input {...field} />}
            name="artistName"
            control={control}
            defaultValue=""
            className="materialUIInput"
            />
         </section>
         <label>Playlist Name</label>
         <section>
            <Controller
            render={({ field }) => <Input {...field} />}
            name="playlistName"
            control={control}
            defaultValue=""
            className="materialUIInput"
            />
         </section>
         <label>Tempo</label>
         <Controller
         name="tempo"
         control={control}
         render={({ field }) => (
               <RadioGroup aria-label="tempo" {...field}>
                  <div className='container'>
                     <section>
                        <FormControlLabel
                           value="0"
                           control={<Radio color='primary'/>}
                           label="Decrease"
                           className='tempoButtons'
                        />
                     </section>

                     <section>
                        <FormControlLabel 
                           value="1" 
                           control={<Radio color='primary'/>} 
                           label="Increase" 
                        />
                  </section>
               </div>
               </RadioGroup>
            )}

         />
         <label>Playlist Length (songs)</label>
         <Controller
            name="length"
            control={control}
            defaultValue={5}
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
         <section>
            <button type="submit">
               Submit
            </button>
         </section>
      </form>
    </div>
  );
};


export default App;