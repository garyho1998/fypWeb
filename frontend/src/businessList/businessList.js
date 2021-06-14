import {
  Grid,
  List,
  ListItem,
  ListItemText,
  ListSubheader,
} from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  businessList: {
    maxHeight: 500,
    overflow: "auto",
    border: "2px solid #eeeeee",
    backgroundColor: theme.palette.background.paper,
  },
  subheader: { textAlign: "left", marginBottom: "10px" },
}));

export default function BusinessList(props) {
  const classes = useStyles();
  return (
    <List className={classes.businessList} subheader={<li />}>
      <ListSubheader className={classes.subheader}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <h5>Business Need</h5>
          </Grid>
        </Grid>
      </ListSubheader>
      {props.businessMatchs && props.businessMatchs.length > 0 ? (
        <div className="align-grid">
          <div className="grid">
            {props.businessMatchs.map((x) => {
              return (
                <div opacity>
                  <ListItem
                    key={x["Reference Code"]}
                    button
                    selected={props.selectedID === x["Reference Code"]}
                    onClick={(event) =>
                      props.handleBusinessMatchClick(event, x["Reference Code"])
                    }>
                    <ListItemText
                      primary={x["Title (Eng)"]}
                      secondary={x["Reference Code"]}
                    />
                  </ListItem>
                </div>
              );
            })}
          </div>
        </div>
      ) : (
        <div className="mt-5 text-center">No businessMatch</div>
      )}
    </List>
  );
}
