import { Main } from "./main/main";
import { BrowserRouter, Route, Switch } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/">
          <Main />
        </Route>
        <Route exact path="/resultedITList">
          <Main page="resultedITList" />
        </Route>
        <Route exact path="/businessList">
          <Main page="businessList" />
        </Route>
        <Route>
          <Main notFound={true} />
        </Route>
      </Switch>
    </BrowserRouter>
  );
}

export default App;
