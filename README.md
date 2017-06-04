# patcher

## Actions
`++`, works for adding a file and replacing (not tested yet)
`--`, removes a file
`>>`, moves a file from one location to another or renames a file (not tested yet)

## Commit Messages
* [Prefixing messages with emoji's.](https://gitmoji.carloscuesta.me/)
* [Imperative subject line](https://chris.beams.io/posts/git-commit/#imperative)

## Tests
The root directory of a test should indicate the purpose of the test.

**Format**
```
operation_type_location_naming
```
* operation - An action (`++`, `--`, or `>>`) can sometime perform multiple types of operation. For example the `++` can both add a new file or update an existing one. To be specific about what the test is supposed to evaluate we use the operation name rather than the action name.
* type - File or directory.
* location - The level of directory nesting that is being tested. Examples, root, sub, or nested.
* naming - The type of naming pattern that is being tested.
	* Standard, an alphabetical word in lower case.
	* Spaces, a lower case name containing at least one white space.

**Examples**
```
add_file_root_standard
remove_di
```

### Naming
To keep the file/directory names consistent and not having to think something up the list below will provide names.

#### Files
Based upon fruits. Inspiration taken from [Wikipedia](https://simple.wikipedia.org/wiki/List_of_fruits).
* apple
* blueberry
* coconut
* dragonfruit
* elderberry
* fig
* grape
* huckleberry
* jackfruit
* kiwi
* lemon
* melon
* nectarine
* orange
* pear
* quince
* raspberry
* strawberry
* tamarind
* ugli
* yuzu


#### Directories
Based upon emotions. Inspiration taken from the article [A List of Feeling Words From A to Z](https://www.thespruce.com/feelings-words-from-a-to-z-2086647).
* awe
* brave
* curious
* delighted
* excited
* frustrated
* greedy
* happy
* irrational
* jinxed
* kind
* lazy
* mad
* nervous
* overstimulated
* psyched
* quirky
* rebellious
* serious
* trusted
* understood
* vibrant
* worried
* xenophobic
* yearning
* zealous
