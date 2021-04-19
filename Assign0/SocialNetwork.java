// Ashutosh Kumar Singh
// 19CS30008
// Software Engineering Lab - Assignment 0

import java.util.*;

public class SocialNetwork
{
	// hashmap to store all the nodes mapped with their IDs, so the unique ID is the key, and the reference to the node object is the value in the hashmap
	HashMap<Integer, Node> nodeList; // ID -> node
	public static void main(String[] args)
	{
		SocialNetwork socNetObj = new SocialNetwork();
		Scanner in = new Scanner(System.in);
		socNetObj.nodeList = new HashMap<Integer, Node>();
		System.out.println("\n*** FOR A BETTER EXPERIENCE PLEASE USE AN ENLARGED / FULL SCREEN TERMINAL WINDOW ***");
		socNetObj.displayMenu();
		int choice = in.nextInt();

		// explore the various functionalities using a switch-case block
		
		while(choice != 10)
		{
			switch(choice)
			{
				case 1 :
					Node newNode = socNetObj.createNode(in);
					if(newNode != null)
					{
						socNetObj.nodeList.put(newNode.id, newNode);
						System.out.println("\n*** Node successfully created! ***");
					}
					break;
				
				case 2 : 
					socNetObj.deleteNode(in);
					break;

				case 3 : 
					socNetObj.addLink(in);
					break;

				case 4 : 
					socNetObj.searchNode(in);
					break;
				
				case 5 : 
					socNetObj.displayLinkedNodes(in);
					break;

				case 6 : 
					socNetObj.createContent(in);
					break;

				case 7 : 
					socNetObj.findContent(in);
					break;

				case 8 : 
					socNetObj.displayLinkedContent(in);
					break;
				
				case 9 : 
					socNetObj.displayAllNodes();
					break;

				default : 
					System.out.println("\n*** Invalid choice! ***");
			}
			socNetObj.displayMenu();
			choice = in.nextInt();
		}
		System.out.println("\n*** THANK YOU! ***\n");
	}

	// function which displays the functionality menu
	public void displayMenu()
	{
		System.out.println("\n*** FUNCTIONALITY MENU ***");
		System.out.println("Enter the appropriate number for any functionality");
		System.out.println("1. Create a node");
		System.out.println("2. Delete a node");
		System.out.println("3. Add a link between two nodes");
		System.out.println("4. Search for nodes using the name or type or birthday");
		System.out.println("5. Print all linked nodes to a given input node");
		System.out.println("6. Create and post content by a user");
		System.out.println("7. Search for content posted by any node");
		System.out.println("8. Display all content posted by nodes linked to a given node");
		System.out.println("9. Display all nodes");
		System.out.println("10. Exit\n");
	}

	// function to check if a given ID exists or not
	public boolean isValidID(int checkID)
	{
		return(nodeList.containsKey(checkID));
	}

	// function to create a node (object) of the desired class
	public Node createNode(Scanner in)
	{
		System.out.println("\nEnter the type of node to be created");
		System.out.print("Enter I for Individual, B for Business, O for organisation, G for group (in either upper or lower case) : ");
		char type = in.next().charAt(0);
		type = Character.toUpperCase(type);
		if(type == 'I')
			return new Individual(in);
		else if(type == 'B')
			return new Business(in);
		else if(type == 'O')
			return new Organisation(in);
		else if(type == 'G')
			return new Group(in);
		else
		{
			System.out.println("\n*** Invalid choice! ***");
			return null;
		}
	}

	// function to delete a specific node, given the unique ID of the node
	public void deleteNode(Scanner in)
	{
		System.out.print("\nEnter the unique ID of the node to be deleted : ");
		int delID = in.nextInt();
		// check if the ID is valid or not
		if(!this.isValidID(delID))
		{
			System.out.println("\n*** Node with ID " + delID + " does not exist! ***");
			return;
		}
		Node delObj = nodeList.get(delID); // the node to be deleted

		// remove the links from all other nodes to which the node to be deleted is linked, by traversing the hashmap containing all the nodes
		for(Map.Entry<Integer, Node> currEntry : nodeList.entrySet())
		{
			if(currEntry.getKey() == delID) // skip the node which we are deleting, as that entire object has to be deleted
				continue;
			if(currEntry.getValue().links.containsKey(delObj))
				currEntry.getValue().links.remove(delObj);
		}

		// set the reference of the object to be deleted to null
		delObj = null;
		// remove the node form the hashmap
 		nodeList.remove(delID);
		System.out.println("\n*** Node with ID " + delID + " successfully deleted! ***");
	}

	// function to add a link between two nodes
	/*
	VALID LINKS : 
	groups - individuals
	groups - business
	organisations - individuals
	business - individuals as owners or customers
	*/
	public void addLink(Scanner in)
	{
		// take the IDs as input and check their validity
		System.out.print("\nEnter node from which you want to create a link : ");
		int fromID = in.nextInt();
		if(!this.isValidID(fromID))
		{
			System.out.println("\n*** Node with ID " + fromID + " does not exist! ***");
			return;
		}
		System.out.print("Enter node to which you want to create a link : ");
		int toID = in.nextInt();
		if(!this.isValidID(toID))
		{
			System.out.println("\n*** Node with ID " + toID + " does not exist! ***");
			return;
		}

		// extract the nodes and their types (classes of which they are an object)
		Node obj1 = nodeList.get(fromID);
		Node obj2 = nodeList.get(toID);

		// the statement obj.getClass().getName() returns the name of the class of which obj is an object
		String type1 = obj1.getClass().getName();
		String type2 = obj2.getClass().getName();

		// if this link already exists, no need to do anything
		if(obj1.links.containsKey(obj2) && obj2.links.containsKey(obj1))
		{
			System.out.println("\n*** This link already exists! ***");
			return;
		}

		// checking if the link is allowed or not
		if((type1.equals("Group") && type2.equals("Individual")) || type1.equals("Individual") && type2.equals("Group") || 
			(type1.equals("Group") && type2.equals("Business")) || type1.equals("Business") && type2.equals("Group") || 
			(type1.equals("Organisation") && type2.equals("Individual")) || type1.equals("Individual") && type2.equals("Organisation"))
		{
			obj1.links.put(obj2, "Member");
			obj2.links.put(obj1, "Member");
			System.out.println("\n*** Link between Node " + fromID + " of type " + type1 + " and Node " + toID + " of type " + type2 + " successfully created! ***");
			System.out.println("*** Relationship - Member ***");
		}
		else if((type1.equals("Business") && type2.equals("Individual")) || type1.equals("Individual") && type2.equals("Business"))
		{
			System.out.println("Enter the type of relationship");
			System.out.print("Enter 1 for Customer or 2 for Owner : ");
			int choice = in.nextInt();
			if((choice != 1) && (choice != 2))
			{
				System.out.println("*** Invalid choice! ***");
				return;
			}
			String relation = ((choice == 1) ? "Customer" : "Owner");
			obj1.links.put(obj2, relation);
			obj2.links.put(obj1, relation);
			System.out.println("\n*** Link between Node " + fromID + " of type " + type1 + " and Node " + toID + " of type " + type2 + " successfully created! ***");
			System.out.println("*** Relationship - " + relation + " ***");
		}
		else
		{
			System.out.println("\n*** Node " + fromID + " is of type " + type1 + " and " + "Node " + toID + " is of type " + type2 + " ***");
			System.out.println("*** This link is not allowed! ***");
		}
	}

	// function to search for a node by name, type or birthday
	public void searchNode(Scanner in)
	{
		System.out.print("\nEnter 1 to search by name, 2 to search by type, 3 to search by birthday : ");
		int choice = in.nextInt();
		boolean found = false; // boolean variable to denote if the search has been successfull or not
		switch(choice)
		{
			// to search by name
			case 1 : 
				System.out.print("Enter name to be searched : ");
				in.nextLine();
				String searchName = in.nextLine();
				for(Map.Entry<Integer, Node> currEntry : nodeList.entrySet())
				{
					if(currEntry.getValue().name.equals(searchName))
					{
						if(!found)
						{
							found = true;
							System.out.println("\n*** Search successfull! ***\n");
						}
						System.out.println(currEntry.getValue());
					}
				}
				break;

			// to search by type
			case 2 : 
				System.out.println("Enter type to be searched : ");
				System.out.print("Enter I for Individual, B for Business, O for organisation, G for group (in either upper or lower case) : ");
				char type = in.next().charAt(0);
				type = Character.toUpperCase(type);
				for(Map.Entry<Integer, Node> currEntry : nodeList.entrySet())
				{
					char currType = currEntry.getValue().getClass().getName().charAt(0);
					// just check the first characters to identify the type of node
					if(currType == type)
					{
						if(!found)
						{
							found = true;
							System.out.println("\n*** Search successfull! ***\n");
						}
						System.out.println(currEntry.getValue());
					}
				}
				break;

			// to search by birthday
			case 3 : 
				System.out.print("Enter birthday to be searched : ");
				in.nextLine();
				String searchBirthday = in.nextLine();
				for(Map.Entry<Integer, Node> currEntry : nodeList.entrySet())
				{
					// only objects of class Individual can have birthday as an attribute
					if(currEntry.getValue().getClass().getName().equals("Individual"))
					{
						Individual obj = (Individual)currEntry.getValue();
						if(obj.birthday.equals(searchBirthday))
						{
							if(!found)
							{
								found = true;
								System.out.println("\n*** Search successfull! ***\n");
							}
							System.out.println(obj);
						}
					}
				}
				break;
			
			default : 
				System.out.println("\n*** Invalid choice! ***");
				return;
		}
		if(!found)
			System.out.println("\n*** Search unsuccessfull! ***");
	}

	// function to display details of all nodes linked to a specific node
	public void displayLinkedNodes(Scanner in)
	{
		System.out.print("\nEnter node ID for which all linked nodes are to be displayed : ");
		int viewID = in.nextInt();
		if(!this.isValidID(viewID))
		{
			System.out.println("\n*** Node with ID " + viewID + " does not exist! ***");
			return;
		}
		Node currObj = nodeList.get(viewID);
		// if no nodes are linked to this node
		if(currObj.links.size() == 0)
		{
			System.out.println("\n*** No linked nodes to node with ID " + viewID + " exist! ***");
			return;
		}
		System.out.println("\n*** Nodes linked to node with ID " + viewID + " : ***");

		// iterating through the hashmap storing the links to print all linked nodes
		for(Map.Entry<Node, String> currEntry : currObj.links.entrySet())
		{
			System.out.println();
			System.out.println("Unique ID : " + currEntry.getKey().id);
			System.out.println("Type : " + currEntry.getKey().getClass().getName());
			System.out.println("Name : " + currEntry.getKey().name);
			System.out.println("Relationship : " + currEntry.getValue());
		}
	}

	// function to create new content for a specific node
	public void createContent(Scanner in)
	{
		System.out.print("\nEnter node ID for which you want to post content : ");
		int nodeID = in.nextInt();
		if(!this.isValidID(nodeID))
		{
			System.out.println("\n*** Node with ID " + nodeID + " does not exist! ***");
			return;
		}
		System.out.print("Enter content to be posted : ");
		in.nextLine();
		String post = in.nextLine();

		// if that post is already present, we do not have to add it again
		if(nodeList.get(nodeID).content.contains(post))
			System.out.println("\n*** This post is already present! ***");
		else
		{
			nodeList.get(nodeID).content.add(post);
			System.out.println("\n*** Content successfully posted! ***");
		}
	}

	// function to search / view content for a node
	public void findContent(Scanner in)
	{
		System.out.print("\nEnter node ID for which you want to search / view content : ");
		int nodeID = in.nextInt();
		if(!this.isValidID(nodeID))
		{
			System.out.println("\n*** Node with ID " + nodeID + " does not exist! ***");
			return;
		}
		Node currObj = nodeList.get(nodeID);

		// 1 - Take a string as input and check if this is present in the set of content of that node or not
		// 2 - View the entire set of content for this node
		System.out.println("Enter 1 to search a specific content for this node, or 2 to view all the content for this node : ");
		int choice = in.nextInt();

		// to search for some content
		if(choice == 1)
		{
			System.out.print("Enter content to be searched : ");
			in.nextLine();
			String searchCont = in.nextLine();
			if(currObj.content.contains(searchCont))
				System.out.println("\n*** \"" + searchCont + "\" is present in the contents of Node " + nodeID + "! ***");
			else
				System.out.println("\n*** \"" + searchCont + "\" is not present in the contents of Node " + nodeID + "! ***");
		}

		// to view all the content for a specific node
		else if(choice == 2)
		{
			if(currObj.content.size() == 0)
				System.out.println("\n*** No content exists for node with ID " + nodeID + "! ***");
			else
			{
				System.out.println("\nContent for node with ID " + nodeID);
				System.out.println(currObj.content);
			}
		}
		else
			System.out.println("\n***Invalid Choice!***");
	}

	// function to display contents of all nodes linked to a specific node
	public void displayLinkedContent(Scanner in)
	{
		System.out.print("\nEnter node ID for which you want to view content of all its linked nodes : ");
		int nodeID = in.nextInt();
		if(!this.isValidID(nodeID))
		{
			System.out.println("\n*** Node with ID " + nodeID + " does not exist! ***");
			return;
		}
		Node currObj = nodeList.get(nodeID);

		// if no nodes are linked to this node
		if(currObj.links.size() == 0)
		{
			System.out.println("\n*** No linked nodes to node with ID " + nodeID + " exist! ***");
			return;
		}
		System.out.println("\n*** Nodes linked to node ID " + nodeID + " with their content ***");

		// traversing the hashmap of links to display the contents of the linked nodes
		for(Map.Entry<Node, String> currEntry : currObj.links.entrySet())
		{
			System.out.println();
			System.out.println("Unique ID : " + currEntry.getKey().id);
			System.out.println("Type : " + currEntry.getKey().getClass().getName());
			System.out.println("Name : " + currEntry.getKey().name);
			System.out.println("Relationship : " + currEntry.getValue());
			if(currEntry.getKey().content.size() == 0)
				System.out.println("No content exists for this node");
			else
				System.out.println("Content : " + currEntry.getKey().content);
		}
	}

	// function to display all the nodes currently present
	public void displayAllNodes()
	{
		// if no nodes are present
		if(nodeList.size() == 0)
		{
			System.out.println("\n*** No nodes are currently present ***");
			return;
		}
		System.out.println("\n*** Displaying all nodes ***\n");
		for(Map.Entry<Integer, Node> currEntry : nodeList.entrySet())
			System.out.println(currEntry.getValue());
		System.out.println("*** All nodes displayed ***");
	}
}

class Node
{
	int id; // the unique ID for each node
	String name; // the name of the individual, business, group or organisation
	Date creationDate; // creation date of each node
	HashSet<String> content; // a set of strings to store the contents as strings, posted by each user
	HashMap<Node, String> links; // hashmap to store the linked nodes, the Node is the reference of the linked node, and the String is the type of relationship - member, customer or owner

	static int nodesCreated = 0; // a static variable to store the number of nodes created till now to help in generating the unique ID

	// constructor of class Node
	public Node(Scanner in)
	{
		// The unique IDs are consecutive integers like 1, 2, 3, ...
		System.out.println("\nThe unique ID for this node is : " + (nodesCreated + 1));
		this.id = nodesCreated + 1;
		nodesCreated++;
		System.out.print("Enter name : ");
		in.nextLine();
		this.name = in.nextLine();
		this.creationDate = new Date();
		content = new HashSet<String>();
		links = new HashMap<Node, String>();
	}

	// function to help in printing the attributes of an object
	@Override
	public String toString()
	{
		String outString = "Unique ID : " + this.id + "\nType : " + this.getClass().getName() + "\nName : " + this.name + "\nCreation Date : " + this.creationDate;
		return outString;
	}

}

// The class Individual inherits from the class Node
class Individual extends Node
{
	String birthday; // birthday of the individual

	public Individual(Scanner in)
	{
		super(in); // calling the constructor of the parent Node class
		System.out.print("Enter birthday (DD/MM/YYYY) : ");
		this.birthday = in.nextLine();
	}

	@Override
	public String toString()
	{
		String outString = super.toString() + "\nBirthday : " + this.birthday + "\n";
		return outString;
	}
}

// The class Business inherits from the class Node
class Business extends Node
{
	// co-ordinates of the location
	int x_coordinate;
	int y_coordinate;

	public Business(Scanner in)
	{
		super(in); // calling the constructor of the parent Node class
		System.out.println("Enter coordinaes of location");
		System.out.print("Enter x-coordinate : ");
		this.x_coordinate = in.nextInt();
		System.out.print("Enter y-coordinate : ");
		this.y_coordinate = in.nextInt();
	}

	@Override
	public String toString()
	{
		String outString = super.toString() + "\nLocation : (" + this.x_coordinate + ", " + this.y_coordinate + ")\n";
		return outString;
	}
}

// The class Organisation inherits from the class Node
class Organisation extends Node
{
	// co-ordinates of the location
	int x_coordinate;
	int y_coordinate;
	
	public Organisation(Scanner in)
	{
		super(in); // calling the constructor of the parent Node class
		System.out.println("Enter coordinaes of location");
		System.out.print("Enter x-coordinate : ");
		this.x_coordinate = in.nextInt();
		System.out.print("Enter y-coordinate : ");
		this.y_coordinate = in.nextInt();
	}

	@Override
	public String toString()
	{
		String outString = super.toString() + "\nLocation : (" + this.x_coordinate + ", " + this.y_coordinate + ")\n";
		return outString;
	}
}

// The class Group inherits from the class Node
class Group extends Node
{
	public Group(Scanner in)
	{
		super(in); // calling the constructor of the parent Node class
	}

	@Override
	public String toString()
	{
		String outString = super.toString() + "\n";
		return outString;
	}
}