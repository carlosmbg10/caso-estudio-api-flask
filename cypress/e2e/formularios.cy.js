describe("Formulario 1: nombre y apellido", () => {
  beforeEach(() => {
    cy.visit("/index.html");
  });

  it("muestra el nombre completo con datos válidos", () => {
    cy.get("#nombre").type("Carlos");
    cy.get("#apellido").type("Bañol");
    cy.get("#form-persona").submit();

    cy.get("#resultado-persona")
      .should("be.visible")
      .and("have.class", "exito")
      .and("contain.text", "Carlos Bañol");
  });

  it("muestra un error con datos inválidos (campos vacíos)", () => {
    cy.get("#nombre").clear();
    cy.get("#apellido").clear();
    cy.get("#form-persona").submit();

    cy.get("#resultado-persona")
      .should("be.visible")
      .and("have.class", "error");
  });
});

describe("Formulario 2: salario", () => {
  beforeEach(() => {
    cy.visit("/index.html");
  });

  it("calcula el salario neto como el 80% del bruto con datos válidos", () => {
    const bruto = 1000000;
    const netoEsperado = bruto * 0.8;

    cy.get("#salario").type(String(bruto));
    cy.get("#form-salario").submit();

    cy.get("#resultado-salario")
      .should("be.visible")
      .and("have.class", "exito")
      .and("contain.text", String(netoEsperado));
  });

  it("muestra un error con un salario inválido (negativo)", () => {
    cy.get("#salario").type("-500");
    cy.get("#form-salario").submit();

    cy.get("#resultado-salario")
      .should("be.visible")
      .and("have.class", "error");
  });
});

describe("Formulario 3: edad", () => {
  beforeEach(() => {
    cy.visit("/index.html");
  });

  it("muestra la edad calculada con una fecha válida", () => {
    cy.get("#fecha_nacimiento").type("1998-05-20");
    cy.get("#form-edad").submit();

    cy.get("#resultado-edad")
      .should("be.visible")
      .and("have.class", "exito")
      .and("contain.text", "años");
  });

  it("muestra un error con una fecha de nacimiento futura", () => {
    cy.get("#fecha_nacimiento").type("2999-01-01");
    cy.get("#form-edad").submit();

    cy.get("#resultado-edad")
      .should("be.visible")
      .and("have.class", "error");
  });
});
