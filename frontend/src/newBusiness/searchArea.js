import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Grid, TextField, Box, Fab, withStyles } from "@material-ui/core";
import SearchIcon from "@material-ui/icons/Search";
import IconButton from "@material-ui/core/IconButton";
import InputAdornment from "@material-ui/core/InputAdornment";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    width: "90%",
    position: "absolute",
    left: "5%",
    top: "15%",
    "@media (min-width: 1500px)": {
      // width: "70%",
      // left: "15%",
    },
  },
  fab: {
    position: "absolute",
    bottom: "12.5%",
    right: "11%",
  },
  notchedOutline: {
    borderWidth: "2px",
    borderColor: "#1769aa !important",
  },
  box: {
    alignItems: "center",
    paddingLeft: "50px",
    paddingRight: "50px",
    paddingBottom: "100px",
  },
  description: {
    textAlign: "left",
    marginLeft: "15%",
    marginRight: "15%",
    marginBottom: "40px",
  },
  title: {
    textAlign: "left",
    marginLeft: "15%",
    marginRight: "15%",
    marginBottom: "10px",
    fontWeight: "bold",
  },
  inputtext: {
    marginTop: "15%",
    marginLeft: "5%",
    marginRight: "5%",
    width: "90%",
  },
}));
const CssTextField = withStyles({
  root: {
    "& label.Mui-focused": {
      color: "rgb(172, 172, 172)",
    },
    "& .MuiInput-underline:after": {
      borderBottomColor: "rgb(172, 172, 172)",
    },
    "& .MuiOutlinedInput-root": {
      "& fieldset": {
        borderColor: "rgb(172, 172, 172)",
        borderRadius: 15,
        borderWidth: "2px",
      },
      "&:hover fieldset": {
        borderColor: "rgb(172, 172, 172)",
      },
      "&.Mui-focused fieldset": {
        borderColor: "rgb(172, 172, 172)",
      },
    },
  },
})(TextField);
export default function SearchArea(props) {
  const classes = useStyles();
  const handleChange = (event) => {
    props.setbusinessParagraph(event.target.value);
  };
  return (
    <div className={classes.root}>
      <h1 className={classes.title} style={{ color: "#3D4B53" }}>
        Intelligent matching of business needs and IT solutions
      </h1>
      <br />
      <h2 className={classes.description} style={{ color: "#397EA8" }}>IT solutions Searching Engine </h2>
      <Box className={classes.box}>
        <Grid container spacing={3} justify="center" alignItems="center">
          <Grid item xs={9}>
            <CssTextField
              InputProps={{
                endAdornment: (
                  <InputAdornment>
                    <IconButton>
                      <SearchIcon 
                      onClick={(event) => props.handleSearchClick(event)}/>
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              multiline
              className={classes.inputtext}
              label="Search by Business Needs"
              variant="outlined"
              id="custom-css-outlined-input"
              style={{
                backgroundColor: "rgb(156, 190, 211)",
                borderRadius: 15,
              }}
              onChange={handleChange}
              value={props.businessParagraph}
            />
          </Grid>
        </Grid>
      </Box>
    </div>
  );
}
