import { Grid, List, ListSubheader } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import SolutionItem from "./solutionItem";

const useStyles = makeStyles((theme) => ({
  solutionList: {
    maxHeight: 500,
    overflow: "auto",
    border: "2px solid #eeeeee",
    backgroundColor: theme.palette.background.paper,
  },
  subheader: { textAlign: "left", marginBottom: "10px" },
}));

export default function SolutionList(props) {
  const classes = useStyles();

  return (
    <List className={classes.solutionList} subheader={<li />}>
      <ListSubheader className={classes.subheader}>
        <Grid container spacing={3}>
          <Grid item xs={3}>
            <h5>Solution Name</h5>
          </Grid>
          <Grid item xs={7}>
            <h5>Description</h5>
          </Grid>
          <Grid item xs={2}>
            <h5>Cosine Similarity</h5>
          </Grid>
        </Grid>
      </ListSubheader>
      {props.itSolutions && props.itSolutions.length > 0 ? (
        <div className="align-grid">
          <div className="grid">
            {props.itSolutions.map((x) => {
              console.log(x);
              return (
                <SolutionItem
                  id={x["Reference Code"]}
                  name={x["Solution Name (Eng)"]}
                  description={x["Solution Description"]}
                  similarity={x["Cosine Similarity"]}></SolutionItem>
              );
            })}
          </div>
        </div>
      ) : (
        <div className="mt-5 text-center">
          Please Select or Search a Business Need
        </div>
      )}
    </List>
  );
}
