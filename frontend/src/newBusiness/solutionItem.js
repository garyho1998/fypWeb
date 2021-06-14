import { Grid, ListItem, ListItemText } from "@material-ui/core";
import { useState, useEffect } from "react";
import { getSolution } from "../component/businessDao";

export default function SolutionItem(props) {
  var anwswerList = [];
  if (props.answer) {
    var answers = props.answer.substring(1, props.answer.length - 1).split(",");
    answers.forEach((answer) => {
      console.log("answer:", answer);
      anwswerList = anwswerList.concat(answer.split(" "));
    });
  }
  const [itSolution, setitSolution] = useState([]);
  useEffect(() => {
    console.log("render", props.id);
    getSolution(props.id).then((res) => {
      setitSolution(res);
    });
  }, [props.id]);

  return (
    <div>
      {itSolution ? (
        <ListItem key={props.id}>
          <Grid container spacing={3}>
            <Grid item xs={3}>
              <ListItemText
                primary={itSolution["Solution Name (Eng)"]}
                secondary={itSolution["Reference Code"]}
              />
            </Grid>
            <Grid item xs={7}>
              {/* <Highlighter
            highlightClassName="YourHighlightClass"
            searchWords={anwswerList}
            autoEscape={true}
            textToHighlight={props.project}
          /> */}
              <ListItemText primary={itSolution["Solution Description"]} />
              {/* <Highlighter
            text={props.project}
            anwswerList={anwswerList}></Highlighter> */}
            </Grid>
            <Grid item xs={2}>
              <ListItemText primary={props.similarity} />
            </Grid>
          </Grid>
        </ListItem>
      ) : (
        <div className="mt-5 text-center">
          Please Select or Search a Business Need
        </div>
      )}
    </div>
  );
}
