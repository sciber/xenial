# Software Requirements Specification for Xenial


## Introduction

### Purpose
The goal fo the project and objectives it aims to accomplish.

### Document conventions
The typographical methodologies followed within the document. For example any abbreviations, typographical stylization 
of content or change of fonts and its significance.

### Intended audience *(and reading suggestions)* 
Describe which part of the SRS document is intended for which reader. Include a list of all stakeholders of the project, 
developers, project managers, and testers for better clarity. Suggest a sequence for reading the document, beginning with
the overview sections and proceeding through the sections that are most pertinent to each reader type.

### *(Product)* Scope
Specify how the software goals align with the overall business goals and outline the benefits of the project to business.

### References
A list of other documents that the SRS document refers to including sources such as websites or written literature.


## Overall Description

### Product perspective
Describe the context and origin of the product. (State wheter this product is a follow-on member of a product family, a
replacement for certain existing systems, or a new, self-contained product. If the SRS defines a component of a larger
system, terate the requirements of the larger system to the functionality of this software and identify interfaces 
between the two. A simple diagram that shows the major components fo the overall system, subsystem interconnection, and 
external interfaces can be helpful.)

### Product features
A high level summary of the major features product contains and significant functions the software would perform. 
(Details will be provided in Specific Requirements section, so only high level summary is needed here. Organize the 
functions to make them understandable to any reader. A picture of major groups of related requirements and how they 
relate, such as a top level data flow diagram or a class diagram is often effective.)

### User class and characteristics
A categorization and profiling of the users the software is intended for and their classification into different user 
classes. (User classes may be differentiated based on frequency of use, subset of product functions used, technical 
expertise, security or privilege levesl, ecucational level, or experience. describe the pertinent characteristics of each
user class. Distinguish the favored user classes from those who are less important to satisfy.)

### Operating environment
Specification of the environment the software is being to operate in. (This includes hardware platform, operating system 
and versions, and any other software components of applications with which it mst peacefully coexist.)

### Design *(and implementation)* constrains
Any limiting factors that would pose challenge to the development of the software. These include both design as well as
implementation constrains. This factors might include corporate or regulatory policies, hardware limitations (timing 
requirements, memory requirements), interfaces to other applications, specific technologies, tools and databases to be 
used, parallel operations, language requirements, communications protocols, security considerations, design conventions 
or programming standards (e.g. if the customer's organization will be responsible for maintaining the delivered software).

### User documentation
List of the user documentation components (such as user manuals, on-line help, and tutorials) that will be delivered 
along with the software. Identify any known user documentation delivery formats or standards.

### Assumptions and dependencies
A list of all assumptions that you have made regarding the software product and the environment along with any external 
dependencies which my affect the project. The assumed factors (as opposed to known facts) could include third-party or 
commercial components that you paon to use, issues around the development or operating environment, or constraints.
The project could be affected if these assumptions are incorrect, are not shared, or changed. Also identify any
dependencies the project has on external factors, such as software components that you intend to reuse from another 
project, unless they are already documented elsewhere (e.g. in the vision and scope document or the project plan).


## System Features
This section contains the functional requirements for the product by system features--the major services provided by 
the product. It may be organized by  use case, mode of operation user class, object class, functional hierarchy, or 
combinations fo these, whatever makes the most logical sense for your product.

### <System feature 1>

#### Description and priority
Provide a short description of the feature and indicate whether it is of High, Medium, or Low priority. You could also
include specific priority component ratings, such as benefit, penalty, cost, and risk (each rated on a relative scale
from a low of 1 to a high of 9).

#### Stimulus/response sequences
List the sequences of user actions and system repsonses that stimulate the behavior defined for this feature. These will
correspond to the dialog elements associated with the use cases.

#### Functional requirements
Itemize the detailed functional requirements associated with this feature. These are the software capabilities that must
be present in order for the user to carry out the services provided by the feature, or to execute the use case. Include 
how the product should respond to anticipated error conditions or invalid inputs. Requirements should be concise, complete,
unambiguous, verifiable, and necessary. Use "TBD" as a placeholder to indicate when necessary information is not yet 
available. Each requirement should be uniquely indentified with a sequence number or a meaningful tag of some kind.


## External Interface Requirements

### User interfaces
The logic behind the interactions between the users and the software. This includes the sample screen layout, buttons 
and functions that would appear on every screen, messages to be displayed on each screen and the style guides to 
be used. Define the software components for which a user interface is needed. Details of the user interface design 
should be documented in a separate user interface specification.

### Hardware interfaces
All the hardware-software interactions with the list of supported devices on which the software is intended to run on, 
the network requirements along with the list of communication protocols to be used.

### Software interfaces
The interaction of the software to be developed with other software components such as frontend and the backed framework
to be used, the database management system and libraries describing the need and purpose behind each of them.

### Communication interfaces
Determination of all the communication standards to be utilized by the software as a part of the project. Specify any 
communication security of encryption issues, data transfer rates, and synchronization mechanisms.


## Non-Functional Requirements

### Performance requirements
The performance requirements need to be specified for every functional requirement. The rationale behind it also needs 
to be elaborated upon. You may need to state performance requirements for individual functional requirements or features.

### Safety requirements
List out any safeguards that need to be incorporated as a measure against any possible harm the use of the software 
application may cause. Define any user identity authentication requirements. Refer to any external policies or regulations
containing security issues that affect the product. Define any security or privacy certifications that must be satisfied.

### Software quality attributes
Detailing on th additional qualities that need to be incorporated within the software like adaptability,
correctness, flexibility, interoperability, maintainability, portability, reliability, reusability, robustness, testability,
usability etc. Write these to be specific, quantitative, and verifiable when possible. At the least, clarify the relative
preferences for varios attriubutes, such as ease of use over ease of learning.


## Other Requirements
These may include the internationalization requirements, legal requirements, resource utilizations, reuse objectives 
for the project, future updates etc.


## Appendix A: Glossary
Define all the terms necessary to properly interpret this document, including acronyms and abbreviations. You may wish 
to build a separate glossary that spans multiple projects or the entire organization, and just include terms specific to 
a single project in each SRS.


## Appendix B: Analysis Models
Optionally, include any pertinent analysis models, such as data flow diagrams, class diagrams, state-transition diagrams, 
or entity-relationship diagrams.


## Appendix C: Issue List
This is a dynamic list of the open requirements issues that remain to be resolved, including TBDs, pending decisions,
information that is needed, conflicts awaiting resolution, and the like. 


1. Purpose
    1. Definitions
    2. Background
    3. System overview
    4. References
2. Overall description
    1. Product perspective
        1. System Interfaces
        2. User interfaces
        3. Hardware interfaces
        4. Software interfaces
        5. Communication Interfaces
        6. Memory Constraints
    2. Design constraints
        1. Operations
        2. Site Adaptation Requirements
    3. Product functions
    4. User characteristics
    5. Constraints, assumptions and dependencies
3. Specific requirements
    1. External interface requirements
    2. Functional requirements
    3. Performance requirements
    4. Logical database requirement
    5. Software System Attributes
        1. Reliability
        2. Availability
        3. Security
        4. Maintainability
        5. Portability
    6. Functional requirements
        1. functional partitioning
        2. functional description
        3. control description
    7. Environment characteristics
        1. Hardware
        2. peripherals
        3. people
    8. other