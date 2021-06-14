import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { useState, useEffect } from "react";
import { Grid, Box } from "@material-ui/core";

import { getBusinessMatch, getSolutionMatch } from "../component/businessDao";
import SolutionList from "./solutionList";
import BusinessList from "./businessList";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    width: "90%",
    position: "absolute",
    left: "5%",
    top: "15%",
  },
  fab: {
    position: "absolute",
    bottom: "21%",
    right: "11%",
  },
  notchedOutline: {
    borderWidth: "2px",
    borderColor: "#1769aa !important",
  },
  box: {
    alignItems: "center",
    paddingBottom: "100px",
  },
  description: {
    textAlign: "left",
    marginRight: "15%",
    marginBottom: "40px",
  },
  title: {
    textAlign: "left",

    marginRight: "15%",
    marginBottom: "10px",
    fontWeight: "bold",
  },
}));

export default function MatchDataPage() {
  const classes = useStyles();
  const [selectedID, setSelectedID] = React.useState(1);
  const [businessMatchs, setBusinessMatch] = useState([]);
  const [itSolutions, setitSolutions] = useState([]);

  const handleBusinessMatchClick = (event, ID) => {
    getSolutionMatch(ID).then((res) => {
      setitSolutions(res);
    });
    setSelectedID(ID);
  };
  useEffect(() => {
    getBusinessMatch().then((res) => {
      setBusinessMatch(res);
    });
  }, []);

  return (
    <div className={classes.root}>
      <h1 className={classes.title}>Intelligent matching of business needs and IT solutions</h1><br/>
      <h2 className={classes.title}>Existing Business needs’ solutions</h2>
      <p className={classes.description} style={{ color: "#aaaaaa" }}>

      </p>
      <Box className={classes.box}>
        <Grid container spacing={3} justify="center" alignItems="top">
          <Grid item xs={3}>
            <BusinessList
              businessMatchs={businessMatchs}
              selectedID={selectedID}
              handleBusinessMatchClick={
                handleBusinessMatchClick
              }></BusinessList>
          </Grid>
          <Grid item xs={9}>
            <SolutionList itSolutions={itSolutions}></SolutionList>
          </Grid>
        </Grid>
      </Box>
    </div>
  );
}
