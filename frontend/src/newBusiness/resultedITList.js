import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { Box } from "@material-ui/core";
import SolutionList from "../newBusiness/solutionList";

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

export default function ResultedITList(props) {
  const classes = useStyles();
  //   function parseJson(s) {
  //     s.map((x) => {
  //       console.log(x["Reference Code"]);
  //     });
  //   }
  //   try {
  //     parseJson(props.itSolutions);
  //   } catch (e) {
  //     console.log("e:", e);
  //   }
  return (
    <div className={classes.root}>
      <h1 className={classes.title}></h1>Intelligent matching of business needs and IT solutions<br/>
      <h2 className={classes.title}>Resulted IT solutions List</h2>
      <p className={classes.description} style={{ color: "#aaaaaa" }}>
 
      </p>
      <Box className={classes.box}>
        <SolutionList itSolutions={props.itSolutions}></SolutionList>
      </Box>
    </div>
  );
}
