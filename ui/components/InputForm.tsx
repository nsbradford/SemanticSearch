import { faArrowUp } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { useFormik } from 'formik';
import React from 'react';

// interface ErrorType {
//   humanInput?: string;
// }

export function InputForm({
  handleSubmit,
  waiting,
}: {
  handleSubmit: (arg0: string) => void;
  waiting: boolean;
}) {
  //   const validate = (values: any) => {
  //     const errors: ErrorType = {};
  //     if (values.humanInput.length > maxlength) {
  //       errors.humanInput = `Must be ${maxlength} characters or less.`;
  //     } else if (values.humanInput.length == 0) {
  //       errors.humanInput = 'Cannot submit an empty prompt.';
  //     }
  //     return errors;
  //   };

  const formik = useFormik({
    initialValues: {
      humanInput: '',
    },
    // validate,
    onSubmit: (values /* , actions */) => {
      handleSubmit(values.humanInput);
      //   actions.resetForm();
    },
  });

  return (
    <form onSubmit={formik.handleSubmit} className="m-4 mt-10 flex place-content-center">
      <input
        autoComplete="off" // https://gist.github.com/niksumeiko/360164708c3b326bd1c8
        className="w-full max-w-xs shadow appearance-none border rounded  py-2 px-3 mx-1 text-gray-600 leading-tight focus:outline-none focus:shadow-lg"
        id="humanInput"
        name="humanInput"
        placeholder={'ask questions here'}
        onChange={formik.handleChange}
        value={formik.values.humanInput}
        maxLength={80}
        disabled={waiting}
      />

      <button
        type="submit"
        disabled={!formik.isValid || !formik.dirty || waiting}
        className="bg-violet-400 hover:bg-violet-600 text-white font-bold py-2 px-4 rounded focus:outline-slate-400 disabled:bg-slate-200 shadow">
        <FontAwesomeIcon icon={faArrowUp} className="text-base" />
      </button>

      {/* <div className="block">{formik.errors.humanInput}</div> */}
    </form>
  );
}
