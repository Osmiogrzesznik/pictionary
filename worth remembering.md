For Anybody Searching for this error.
I had similar problem.
It can be caused by providing variable as a second parameter in `.on` method that is undefined. Internal code of socket.io tries to call `.apply` method to pass arguments into your event handler. If function registered is not existing and therefore `undefined`, this error occurs since undefined values have no such property . It often may be the case of the typo in the name of the function

i.e

```
socket.on('next_player', this.nextplayer)
```

should be :

```
socket.on('next_player', this.next_player)
```

make sure that

```
this.next_player
```

exists in the moment when the event happens
