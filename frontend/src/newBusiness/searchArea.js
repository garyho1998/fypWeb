import React from "react";
import { useState, useEffect } from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Grid, TextField, Box, Fab } from "@material-ui/core";
import SearchIcon from "@material-ui/icons/Search";
import { getNewBusinessMatch } from "./newBusinessDao";
import LoadingBackdrop from "./loadingBackdrop";

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
}));

export default function SearchArea(props) {
  const classes = useStyles();

  const handleChange = (event) => {
    props.setbusinessParagraph(event.target.value);
  };

  return (
    <div className={classes.root}>
      <h1 className={classes.title}>Search For IT solutions</h1>
      <h3 className={classes.title}>By Deep Learning</h3>
      <p className={classes.description} style={{ color: "#aaaaaa" }}>
        This text is center-aligned on screen widths from 992px and up. This
        text is center-aligned on screen widths from 992px and up. This text is
        center-aligned on screen widths from 992px and up. This text is
        center-aligned on screen widths from 992px and up.
      </p>
      <Box className={classes.box}>
        {" "}
        <Grid container spacing={3} justify="center" alignItems="center">
          <Grid item xs={9}>
            <TextField
              InputProps={{
                classes: {
                  notchedOutline: classes.notchedOutline,
                },
                inputMode: "text",
              }}
              id="outlined-multiline-static"
              label="Business Needs Paragraph"
              multiline
              fullWidth
              rows={15}
              placeholder="input here"
              variant="outlined"
              onChange={handleChange}
              value={props.businessParagraph}
            />
            <Fab
              variant="extended"
              color="primary"
              className={classes.fab}
              onClick={(event) => props.handleSearchClick(event)}>
              <SearchIcon className={classes.extendedIcon} />
              Search
            </Fab>
          </Grid>
        </Grid>
      </Box>
    </div>
  );
}
