import { Grid, Link, ListItem, ListItemText, Box } from "@material-ui/core";
import { useState, useEffect } from "react";
import Highlighter from "../component/highlighter";
import ReadMore from "../component/readmore";

export default function SolutionItem(props) {
  return (
    <div opacity>
      <ListItem key={props.id}>
        <Grid container spacing={3}>
          <Grid item xs={2}>
            <ListItemText primary={props.name} secondary={props.id} />
          </Grid>
          <Grid item xs={4}>
            <ReadMore paragraph={props.description}></ReadMore>
          </Grid>
          <Grid item xs={4}>
            <Highlighter
              text={props.project}
              answer={props.answer}></Highlighter>
          </Grid>

          <Grid item xs={2}>
            <ListItemText primary={props.year} />
          </Grid>
        </Grid>
      </ListItem>
    </div>
  );
}
