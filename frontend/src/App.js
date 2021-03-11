import logo from './logo.svg';
import './App.css';
import React, {useState} from 'react';
import axios from 'axios';
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import PhotoCamera from '@material-ui/icons/PhotoCamera';
import IconButton from '@material-ui/core/IconButton';
import Navigation from './Navigation';
function App() {
  const [predicted, setPredicted] = useState('/test.png');
  const [selectedFile, setSelectedFile] = useState(null);
  const [image, setImage] = useState('/8.png');
  const [score, setScore] = useState(0);

  const submitForm = (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("image", selectedFile);
    axios.post('http://127.0.0.1:5000/predict', formData)
    .then (res => {
      console.log(res);
      setPredicted('data:image/png;base64,' + res.data.data);
      setScore(res.data.score);
    })
    .catch(err => {
      alert(err);
    })
  }

  const setFileAndImage = (file) => {
    setSelectedFile(file);
    if (file != null){
      setImage(URL.createObjectURL(file));
      setPredicted(null);
    } else {
      setImage(null);
      setPredicted(null);

    }
    
    
  }

  const useStyles = makeStyles((theme) => ({
    root: {
      '& > *': {
        margin: theme.spacing(1),
      },
    },
    input: {
      display: 'none',
    },

    paper: {
      padding: theme.spacing(1),
      textAlign: 'center',
      color: 'white',
      fontFamily: 'Menlo',
      fontSize: '20px',
      backgroundColor: '#222'

    },
  }));
  const classes = useStyles();
  
  
 
  return (
    <div className="App">
      <Navigation/>
      <div className ="con">
      
      <div className='Container'>
        
          <Paper className={`grid ${classes.paper}`}>
            <p>{image == null ? "" : "Original"}</p>
            <img src={image}></img>
          </Paper>
       
        
          <Paper className={`grid ${classes.paper}`}>
            <p>{predicted == null ? "": 'Enhanced'}</p>
            <img src = { predicted }></img>
          </Paper>
        
      </div>
      <p className="score">{ score > 0 ? `PNSR: ${score}` : ""}</p>


      <form onSubmit={e => submitForm(e)} >
        <input
          accept="image/*"
          className={classes.input}
          id='icon-button-file'
          type='file'
          onChange={e => setFileAndImage(e.target.files[0])}
          />
          <label htmlFor="icon-button-file">
            <IconButton color="primary" aria-label="upload picture" component="span">
              <PhotoCamera />
            </IconButton>
        </label>
          <br/>
          {console.log(selectedFile)}
          <button type="submit" hidden = { selectedFile == null ? true : false }>

            Enhance!
          </button>
      </form>
      </div>
      
    </div>
  );
}

export default App;
