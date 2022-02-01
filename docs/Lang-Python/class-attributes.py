class Base:
    CLASS_VAR = 'class-value'

    LIST_VAR = ['ciao']

    def get_var(self):
        try:
            print(CLASS_VAR)
        except NameError:
            print('ERROR: This is an expected error...')

        print('...in a method, you have to refer to class variables with the self scope: ' + self.CLASS_VAR)


    def set_var(self):
        self.CLASS_VAR = 'instance-changed-with-method'


b = Base()
print(f'Class and instance data attribute are the same thing')
print(f'  instc: {b.CLASS_VAR} @ {id(b.CLASS_VAR): x}')
print(f'  class: {Base.CLASS_VAR} @ {id(Base.CLASS_VAR): x}')
print()

Base.CLASS_VAR = 'class-changed'
print(f'Changing class attribute affects instance too')
print(f'  instc: {b.CLASS_VAR} @ {id(b.CLASS_VAR): x}')
print(f'  class: {Base.CLASS_VAR} @ {id(Base.CLASS_VAR): x}')
print()


b.CLASS_VAR = '  instance-changed'
print(f'Changing instance attribute does not influence class, it creates a instance-only attribute.\n\
This is because the string is immutable, so when assigning to the instance string, we are creating\n\
a new object string pointed by the instance')
print(f'  instc: {b.CLASS_VAR} @ {id(b.CLASS_VAR): x}')
print(f'  class: {Base.CLASS_VAR} @ {id(Base.CLASS_VAR): x}')
print()

b.set_var()
print('Same thing happen when the change is done in a method')
print(f'  instc: {b.CLASS_VAR} @ {id(b.CLASS_VAR): x}')
print(f'  class: {Base.CLASS_VAR} @ {id(Base.CLASS_VAR): x}')
print()

del b.CLASS_VAR
print(f'Deleting the instance attribute, the scope of the variable name goes back to the class')
print(f'  instc: {b.CLASS_VAR} @ {id(b.CLASS_VAR): x}')
print(f'  class: {Base.CLASS_VAR} @ {id(Base.CLASS_VAR): x}')

b.get_var()
print('')

print('Lets now try to do the same using a mutable type...the list!')
print(f'  instc: {b.LIST_VAR} @ {id(b.LIST_VAR): x}')
print(f'  class: {Base.LIST_VAR} @ {id(Base.LIST_VAR): x}')
print()

b.LIST_VAR.append('append-from-instance')
Base.LIST_VAR.append('append-from-class')
print(f'Changing instance attribute DOES influence class,\n\
This is because the list is mutable')
print(f'  instc: {b.LIST_VAR} @ {id(b.LIST_VAR): x}')
print(f'  class: {Base.LIST_VAR} @ {id(Base.LIST_VAR): x}')
print()

b.LIST_VAR = ['ciao-belli']
print(f'BUT! Assigning a new list to the LIST reference will behave as a string variable!!')
print(f'So, changing instance creates a new object')
print(f'  instc: {b.LIST_VAR} @ {id(b.LIST_VAR): x}')
print(f'  class: {Base.LIST_VAR} @ {id(Base.LIST_VAR): x}')
print()

del b.LIST_VAR
Base.LIST_VAR = ['new-list-by-cls']
print(f'And, changes from class are seen in instance')
print(f'  instc: {b.LIST_VAR} @ {id(b.LIST_VAR): x}')
print(f'  class: {Base.LIST_VAR} @ {id(Base.LIST_VAR): x}')
print()
