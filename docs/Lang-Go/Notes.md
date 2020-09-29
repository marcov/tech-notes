# Golang Notes

## Pretty-print a structure
```
import "encoding/json"

...

s, _ := json.MarshalIndent(structure, "", "\t");
fmt.Print(string(s))
```

## Using `select` with channels
When using `select` for reading from a channel, the `case <- myChan` will be
run ALSO when the channel is closed!

E.g.:
```
go func() {
    //...
    close(myChan)
    //...
}()


select {
    case <- myChan:
        fmt.Println("Read from channel / closed chanel")
}
```
